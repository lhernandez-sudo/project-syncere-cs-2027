"""Course helpers shared by the virtual and physical SunFounder PiCar-X."""

from collections.abc import Callable
from typing import Literal

from vendor.sunfounder_picarx import Picarx

ScanLabel = Literal["human", "stop sign", "clear"]


class CoursePicarx(Picarx):
    """The SunFounder car API plus the course's camera and turning helpers."""

    def scan(self) -> ScanLabel:
        """Read a camera label supplied by the selected environment."""
        raise NotImplementedError("A camera scanner must supply this reading.")

    def turn_left(self, speed: float = 28) -> None:
        self.set_dir_servo_angle(-28)
        self.forward(speed)

    def turn_right(self, speed: float = 28) -> None:
        self.set_dir_servo_angle(28)
        self.forward(speed)


class HardwarePicarx(CoursePicarx):
    """Use SunFounder's motor/sensor implementation and an injected scanner."""

    is_simulation = False

    def __init__(self, scanner: Callable[[], ScanLabel], **hardware_options) -> None:
        self._scanner = scanner
        super().__init__(**hardware_options)

    def scan(self) -> ScanLabel:
        # Keep the motors stopped while a synchronous camera inference runs.
        self.stop()
        label = self._scanner()
        if label not in ("human", "stop sign", "clear"):
            self.stop()
            raise ValueError(f"Camera scanner returned an unsupported label: {label!r}")
        return label
