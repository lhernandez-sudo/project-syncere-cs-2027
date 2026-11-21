"""Camera perception for the course's scan() vocabulary.

Uses COCO-trained YOLO detections, not simulator coordinates. Run with --image
to inspect a photo or --camera picamera2 to test the Pi camera without motors.
"""

import argparse
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import time

from car_api import ScanLabel


@dataclass(frozen=True)
class Detection:
    label: ScanLabel
    confidence: float
    # Normalized image coordinates, from 0 to 1.
    box: tuple[float, float, float, float]


class CameraScanner:
    """Capture, detect, and translate observations into student-facing labels."""

    def __init__(
        self, model: str = "yolo11n.pt", *, confidence: float = 0.45,
        person_hold: float = 0.8, sign_hold: float = 0.4,
        minimum_sign_area: float = 0.005, max_scan_seconds: float = 2.0,
    ) -> None:
        if not 0 < confidence <= 1 or not 0 <= minimum_sign_area <= 1:
            raise ValueError("Confidence and minimum sign area must be between 0 and 1.")
        if (not all(math.isfinite(value) for value in (person_hold, sign_hold, max_scan_seconds))
                or person_hold < 0 or sign_hold < 0 or max_scan_seconds <= 0):
            raise ValueError("Hold durations must be nonnegative and scan timeout positive.")
        from ultralytics import YOLO

        self.model = YOLO(model)
        names = self.model.names
        self.classes = [index for index, name in names.items()
                        if name in ("person", "stop sign")]
        if {names[index] for index in self.classes} != {"person", "stop sign"}:
            raise ValueError("Use a detection model with person and stop sign classes.")
        self.confidence = confidence
        self.person_hold = person_hold
        self.sign_hold = sign_hold
        self.minimum_sign_area = minimum_sign_area
        self.max_scan_seconds = max_scan_seconds
        self.person_until = -1.0
        self.sign_until = -1.0
        self.camera = None
        self.camera_kind = None
        self.last_detections: list[Detection] = []
        self.last_seconds = 0.0

    def detect_frame(self, frame) -> list[Detection]:
        """Return person/stop-sign boxes from a uint8 BGR image."""
        if frame is None or len(frame.shape) != 3 or frame.shape[2] != 3:
            raise RuntimeError("Camera returned an invalid BGR image.")
        result = self.model.predict(
            frame, imgsz=640, conf=self.confidence, classes=self.classes,
            device="cpu", verbose=False,
        )[0]
        boxes = result.boxes
        detections = []
        for class_id, confidence, box in zip(
            boxes.cls.tolist(), boxes.conf.tolist(), boxes.xyxyn.tolist()
        ):
            name = self.model.names[int(class_id)]
            label: ScanLabel = "human" if name == "person" else "stop sign"
            detections.append(Detection(label, confidence, tuple(box)))
        self.last_detections = detections
        return detections

    def select_label(self, detections: list[Detection], now: float) -> ScanLabel:
        """Prioritize people near the path and smooth short detection dropouts."""
        for detection in detections:
            left, top, right, bottom = detection.box
            if detection.label == "human" and right >= 0.15 and left <= 0.85 and bottom >= 0.25:
                self.person_until = now + self.person_hold
            if detection.label == "stop sign":
                area = max(0, right - left) * max(0, bottom - top)
                if area >= self.minimum_sign_area:
                    self.sign_until = now + self.sign_hold
        if now <= self.person_until:
            return "human"
        if now <= self.sign_until:
            return "stop sign"
        return "clear"

    def open_camera(self, kind: str = "picamera2", index: int = 0) -> None:
        """Open a Raspberry Pi CSI camera or an OpenCV USB camera."""
        if self.camera is not None:
            raise RuntimeError("Camera is already open.")
        if kind == "picamera2":
            from picamera2 import Picamera2

            camera = Picamera2()
            try:
                camera.configure(camera.create_video_configuration(
                    main={"size": (640, 480), "format": "RGB888"}, buffer_count=2
                ))
                # Picamera2 RGB888 captures BGR bytes, as required by OpenCV/YOLO.
                camera.start()
            except Exception:
                camera.close()
                raise
        elif kind == "usb":
            import cv2

            camera = cv2.VideoCapture(index)
            if not camera.isOpened():
                camera.release()
                raise RuntimeError(f"Could not open USB camera {index}.")
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        else:
            raise ValueError("Camera kind must be picamera2 or usb.")
        self.camera = camera
        self.camera_kind = kind

    def read_frame(self):
        if self.camera is None:
            raise RuntimeError("Open the camera before scanning.")
        if self.camera_kind == "picamera2":
            return self.camera.capture_array("main")
        success, frame = self.camera.read()
        if not success:
            raise RuntimeError("USB camera failed to return a frame.")
        return frame

    def scan(self) -> ScanLabel:
        """Read a fresh frame and fail explicitly if perception takes too long."""
        started = time.monotonic()
        detections = self.detect_frame(self.read_frame())
        now = time.monotonic()
        self.last_seconds = now - started
        if self.last_seconds > self.max_scan_seconds:
            raise RuntimeError(
                f"Camera scan took {self.last_seconds:.2f}s, exceeding "
                f"{self.max_scan_seconds:.2f}s. Check camera and inference speed."
            )
        return self.select_label(detections, now)

    def close(self) -> None:
        if self.camera is not None:
            try:
                if self.camera_kind == "picamera2":
                    try:
                        self.camera.stop()
                    finally:
                        self.camera.close()
                else:
                    self.camera.release()
            finally:
                self.camera = None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--image", type=Path)
    source.add_argument("--camera", choices=["picamera2", "usb"])
    parser.add_argument("--model", default=str(Path(__file__).with_name("yolo11n.pt")))
    parser.add_argument("--confidence", type=float, default=0.45)
    parser.add_argument("--minimum-sign-area", type=float, default=0.005)
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--seconds", type=float, default=20)
    args = parser.parse_args()
    if not math.isfinite(args.seconds) or args.seconds <= 0:
        parser.error("--seconds must be a positive finite number.")
    scanner = CameraScanner(args.model, confidence=args.confidence,
                            minimum_sign_area=args.minimum_sign_area)
    if args.image:
        import cv2

        frame = cv2.imread(str(args.image))
        detections = scanner.detect_frame(frame)
        print(json.dumps({
            "label": scanner.select_label(detections, time.monotonic()),
            "detections": [asdict(detection) for detection in detections],
        }, indent=2))
        return
    try:
        scanner.open_camera(args.camera, args.camera_index)
        deadline = time.monotonic() + args.seconds
        while time.monotonic() < deadline:
            print(f"{scanner.scan():9} {scanner.last_seconds:.3f}s", flush=True)
    finally:
        scanner.close()


if __name__ == "__main__":
    main()
