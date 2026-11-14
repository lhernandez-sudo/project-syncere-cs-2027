"""Student controller for the Virtual PiCar-X capstone.

Only edit this file during the project. The evaluator imports control_step().
"""


def choose_turn(memory: dict) -> int:
    """Alternate turn direction so the car can escape repeated obstacles."""
    previous_turn = memory.get("turn", 30)
    next_turn = -previous_turn
    memory["turn"] = next_turn
    return next_turn


def control_step(car, memory: dict) -> None:
    """Read sensors and issue one set of driving commands.

    TODO: Improve this baseline. It can avoid a wall directly ahead, but it does
    not navigate every course well and does not yet use the grayscale sensors.
    """
    distance = car.ultrasonic.read()
    line_sensors = car.get_grayscale_data()

    # A negative distance represents a temporary sensor failure.
    if distance < 0:
        car.stop()
        return

    if distance < 24:
        car.set_dir_servo_angle(choose_turn(memory))
        car.backward(35)
    elif distance < 45:
        car.set_dir_servo_angle(memory.get("turn", 30))
        car.forward(24)
    elif line_sensors[0] < line_sensors[1]:
        # The left sensor sees the dark route line.
        car.set_dir_servo_angle(-22)
        car.forward(34)
    elif line_sensors[2] < line_sensors[1]:
        # The right sensor sees the dark route line.
        car.set_dir_servo_angle(22)
        car.forward(34)
    elif line_sensors[1] < 600:
        car.set_dir_servo_angle(0)
        car.forward(48)
    else:
        # Search gently for a line instead of racing while lost.
        car.set_dir_servo_angle(memory.get("turn", 25))
        car.forward(18)
