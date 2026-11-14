# Virtual PiCar-X Navigation Capstone

Build a Python controller for a simulated PiCar-X. Your controller uses the same
kind of commands and sensors as the physical car, but it is tested safely in a
repeatable virtual environment.

## The engineering idea

Aircraft, cars, robots, and industrial systems are tested in simulation before
people trust them in the physical world. The simulator is not the real product;
it is a controlled place to reveal mistakes, compare designs, and test dangerous
or unusual situations.

Your program receives a `car` object. During class, it is a `VirtualPicarx`.
With a physical PiCar-X, the same decision-making function can receive a real
`Picarx` object.

```python
def control_step(car, memory):
    distance = car.ultrasonic.read()

    if distance < 25:
        car.set_dir_servo_angle(30)
        car.backward(30)
    else:
        car.set_dir_servo_angle(0)
        car.forward(45)
```

## Start here

1. Open `student_controller.py`.
2. Complete `control_step()` using variables, conditions, lists or dictionaries,
   loops, and helper functions.
3. From this folder, run the simulator:

   ```bash
   python run_student.py
   ```

4. Watch the replay in your browser. The script runs your controller once under
   the strict rules, starts playback, and shows your automated score out of 90.
   If your browser does not open, open `strict_replay.html` from this folder.
5. Read `score_report.txt`, improve one weakness, and run the same command again.

Use Python 3.12 or newer. The simulator uses Python's standard library and a
regular browser, so there are no packages to install. On Windows, use
`py -3 run_student.py` if `python` does not start Python.

## Two lessons

Run `python run_student.py` for both lessons and rerun it after changing your
controller. Both lessons use the same cul-de-sac course.

1. **Build a safe driver.** Focus on the approach to the turnaround.
   Use `car.scan()` to recognize the stop sign and pedestrian. Use the grayscale
   list to follow the line and the ultrasonic reading to slow or stop before a
   box. Check the replay and explain one decision using an `if` statement.
2. **Navigate the cul-de-sac.** Drive through the 11 checkpoint zones in order, go
   around boxes using either side of the open pavement, and return to the
   entrance. Use a small memory dictionary to remember a turn or recovery state.
   Compare your checkpoint and collision counts across runs.

The strict attempt ends on a collision, missed stop sign, course boundary hit, or
sustained stall. The replay shows the reason and checkpoints earned.

Keep the controller in `control_step(car, memory)`. The steering, motor,
ultrasonic, and grayscale calls follow the PiCar-X interface. On the physical
course, use tape to mark the road edges and cardboard boxes for the obstacles.
The simulated camera labels from `scan()` need a camera adapter on hardware.
Use the grayscale and distance readings to make decisions that can transfer
to the physical course.

## Student-facing API

| Command or sensor | Meaning |
| --- | --- |
| `car.forward(speed)` | Move forward at a speed from 0 to 100. |
| `car.backward(speed)` | Move backward at a speed from 0 to 100. |
| `car.stop()` | Stop both drive motors. |
| `car.set_dir_servo_angle(angle)` | Steer from -35 degrees to +35 degrees. |
| `car.ultrasonic.read()` | Distance to the nearest object ahead in centimeters. |
| `car.get_grayscale_data()` | Three virtual ground-sensor readings: left, center, right. |
| `car.scan()` | Camera result: `"human"`, `"stop sign"`, or `"clear"`. |
| `car.turn_left(speed)` | Readable helper that steers and moves left. |
| `car.turn_right(speed)` | Readable helper that steers and moves right. |
| `memory` | A dictionary that remembers information between simulation steps. |

The student challenge deliberately matches the first six weeks:

- **Variables:** store distance, speed, steering, and sensor readings.
- **Lists:** interpret the three grayscale readings.
- **Conditions:** choose what the car should do next.
- **Loops:** the simulator repeatedly calls the student's function.
- **Functions:** separate sensing, decisions, and movement into readable jobs.
- **Dictionaries:** keep a small amount of memory between steps.
- **Classes:** use the provided `car` object and its methods; students are not
  required to construct the simulator's classes.

The simulator repeatedly calls `control_step()`, so students write the logic
that conceptually belongs inside `while driving():` without creating an infinite
loop that could freeze the shared evaluator:

```python
def control_step(car, memory):
    scan_input = car.scan()

    if scan_input == "human":
        car.stop()
    elif scan_input == "stop sign":
        car.stop()
    else:
        car.forward(35)
```

The simulator also provides `car.is_simulation`, which is useful only for
debugging. Navigation logic should not depend on it.

## Fair testing

The evaluator uses several courses:

- `practice`: visible course for learning the API.
- `slalom`: requires repeated steering decisions.
- `tight_turn`: tests recovery and controlled speed.
- `sensor_fault`: occasionally returns `-1` from the ultrasonic sensor.
- `unseen`: changes obstacle positions using a fixed hidden evaluation seed.

Scores are deterministic: the same code receives the same score. Students may
run the evaluator as often as they want. The goal is documented improvement,
not a mysterious one-shot grade.

## Three-class plan

### Class 1 — Safe baseline

- Inspect the simulator and connect the API to the physical PiCar-X vocabulary.
- Write a controller that starts, steers, stops, and avoids one obstacle.
- Use the practice replay to explain one decision made by the program.
- Commit a working baseline.

### Class 2 — Reliability and competition

- Test slalom, tight-turn, and sensor-fault scenarios.
- Add helper functions and a `memory` state.
- Compare scores without copying code.
- Record one failure, its cause, and the change that fixed it.

### Class 3 — Validation and showcase

- Run the complete evaluator.
- Improve the weakest rubric category.
- Complete the README and engineering reflection.
- Rehearse a two-minute demonstration using the animated replay.

## Scoring rubric

| Category | Points | Evidence |
| --- | ---: | --- |
| Mission completion | 50 | Earns checkpoint credit and reaches the finish on the cul-de-sac course. |
| Safety | 15 | Makes progress while obeying traffic rules and avoiding contact. |
| Robustness | 10 | Makes progress and stops safely without controller errors. |
| Efficiency | 5 | Finishes within the step and steering limits. |
| Code quality | 10 | Uses descriptive names, focused functions, a called helper, and useful documentation. |
| Engineering explanation | 10 | Explains the design, tests, failure evidence, and improvements. |

The automated score uses the strict course rules and gives up to 80 points for
driving behavior and 10 for code quality. Replay checkpoint points show course
progress. The replay and score report show the automated rubric score. The instructor
awards the final 10 points for the demonstration and engineering explanation.

## Required showcase artifacts

- `student_controller.py`
- `score_report.txt`
- `strict_replay.html`
- A short README or reflection describing the approach and one improvement
- Git commits showing a baseline, tested improvement, and final version

## Safety rule

Every controller must stop the car when it finishes or encounters an unsafe
condition. A `try/finally` block is still required when adapting the controller
to real hardware.
