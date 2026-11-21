"""Complete instructor model for the guided Colab course.

Paste this entire file into the student code cell, run it, then run debug.
Expected: 8/8 loop checks, 8/8 driving checks, and 5/5 visual checkpoints.
This is for the guided course, not the advanced cul-de-sac or real hardware.
"""

driver_name = "Captain Cautious"
custom_object = "giant sneaker"
avoid_direction = "left"


# CHECKPOINT 8 — FOR LOOP: check each known stop hazard.
def is_stop_signal(scan_input: str) -> bool:
    stop_labels = ["human", "stop sign"]
    for hazard in stop_labels:
        if scan_input == hazard:
            return True
    return False  # Only after checking every label.


# CHECKPOINT 9 — WHILE LOOP: build a launch countdown.
def launch_countdown(start: int) -> list:
    countdown = []
    seconds_left = start
    while seconds_left > 0:
        countdown.append(seconds_left)
        seconds_left = seconds_left - 1
    return countdown


def control_step(car, memory: dict) -> None:
    """Read both sensors, handle hazards, then move when allowed."""
    # Checkpoint 1: read fresh sensor values.
    scan_input = car.scan()
    distance = car.ultrasonic.read()

    # Checkpoints 2 and 3 use the for-loop helper from checkpoint 8.
    if is_stop_signal(scan_input):
        car.stop()
        return

    # Checkpoint 4: distance has priority over going around your object.
    if distance < 25:
        car.stop()
        return

    # Checkpoint 7: the personal object is handled before unknown words.
    if scan_input == custom_object:
        if avoid_direction == "left":
            car.set_dir_servo_angle(-25)
        else:
            car.set_dir_servo_angle(25)
        car.forward(30)
        return

    # Checkpoint 5: stop for an unfamiliar reading.
    if scan_input != "clear":
        car.stop()
        return

    # Checkpoint 6: reset steering after a detour, then drive.
    car.set_dir_servo_angle(0)
    car.forward(30)


my_test = [
    ("clear", 100),
    ("human", 70),
    ("stop sign", 70),
    (custom_object, 70),
    (custom_object, 10),
    ("clear", 100),
]

print("Working guided controller loaded. Run the notebook debug or replay cell next.")
