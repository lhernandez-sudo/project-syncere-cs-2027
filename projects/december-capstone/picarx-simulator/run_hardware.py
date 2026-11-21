"""Run the same student controller on a Raspberry Pi with a real PiCar-X."""

import argparse
import importlib
import time

from car_api import HardwarePicarx
from run_simulation import HERE, load_controller


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scanner",
                        help="Camera adapter as module:function, returning a course scan label.")
    parser.add_argument("--camera", choices=["picamera2", "usb"], default="picamera2")
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--model", default=str(HERE / "yolo11n.pt"))
    parser.add_argument("--seconds", type=float, default=30)
    args = parser.parse_args()
    if not 0 < args.seconds <= 300:
        parser.error("--seconds must be greater than zero and at most 300.")
    controller = load_controller(HERE / "student_controller.py")
    camera = None
    if args.scanner:
        module_name, separator, function_name = args.scanner.partition(":")
        if not separator:
            parser.error("--scanner must use module:function.")
        scanner = getattr(importlib.import_module(module_name), function_name)
        if not callable(scanner):
            parser.error("The scanner must be callable.")
    else:
        from camera_scanner import CameraScanner
        camera = CameraScanner(args.model)
        try:
            camera.open_camera(args.camera, args.camera_index)
            # Warm up model inference before initializing the car's motors.
            camera.detect_frame(camera.read_frame())
        except Exception:
            camera.close()
            raise
        scanner = camera.scan
    car = None
    memory: dict[str, object] = {}
    deadline = time.monotonic() + args.seconds
    try:
        car = HardwarePicarx(scanner)
        while time.monotonic() < deadline:
            started = time.monotonic()
            controller(car, memory)
            time.sleep(max(0, 0.12 - (time.monotonic() - started)))
    finally:
        try:
            if car is not None:
                car.stop()
        finally:
            if camera is not None:
                camera.close()


if __name__ == "__main__":
    main()
