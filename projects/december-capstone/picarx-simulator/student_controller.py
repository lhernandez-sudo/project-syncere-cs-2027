"""Student starter for the Virtual PiCar-X capstone."""


def control_step(car, memory):
    """Drive forward. Add your own rules one at a time."""
    # TODO: Stop at stop signs and yield to pedestrians.
    # TODO: Detect obstacles and steer around them.
    car.set_dir_servo_angle(0)
    car.forward(30)
