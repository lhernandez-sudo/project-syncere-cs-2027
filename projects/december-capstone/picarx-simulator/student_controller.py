"""Student starter for the Virtual PiCar-X capstone."""

from car_api import CoursePicarx


def control_step(car: CoursePicarx, memory: dict[str, object]) -> None:
    """Tell the virtual car what to do for one simulation step.

    Use car methods to steer, drive, or stop. Use memory to keep named
    values between steps, such as memory["stopped"] = True.
    """
    # TODO: Stop at stop signs and yield to pedestrians.
    # TODO: Detect obstacles and steer around them.
    car.set_dir_servo_angle(0)
    car.forward(40)
