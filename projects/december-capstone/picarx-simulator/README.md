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
from car_api import CoursePicarx


def control_step(car: CoursePicarx, memory: dict[str, object]) -> None:
    distance: float = car.ultrasonic.read()

    if distance < 25:
        car.set_dir_servo_angle(30)
        car.backward(30)
    else:
        car.set_dir_servo_angle(0)
        car.forward(45)
```

## Start here

### Camera decision practice in Jupyter or Colab

**Start with the completed example:**
[Open the working Colab](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/projects/december-capstone/picarx-simulator/picarx-working-demo-v2.ipynb).
Run setup, the completed controller, and simulation in order. No edits or
installs are required. Expected result: five of five guided skills checkpoints
and an animated HTML replay. This version has no unfinished checkpoint tasks.
Use it to verify playback before returning to the student exercise below.

Checkpoint 8 uses a `for` loop to inspect stop-hazard labels in
`is_stop_signal()`. Checkpoint 9 uses a terminating `while` loop to build a
launch countdown in `launch_countdown()`. Both helpers live in the same student
code cell, with eight additional debug checks below. Working demos include
completed helpers and call the hazard helper from the controller. The countdown
displays numbers; it does not measure time or control the stop-sign wait.
Allow about ten minutes per loop, or use the countdown as an extension.

Open [picarx-camera-decisions.ipynb](picarx-camera-decisions.ipynb) for a
beginner-friendly, self-contained introduction before the full driving challenge.
Its single student code cell uses checkpoint comments and runnable placeholders.
The initial car stays stopped; failed checks are expected until rules are added.
The [complete instructor model](guided_debug_controller.py) can replace that
entire code cell for verification. Run it and then debug: expected results are
8/8 loop checks, 8/8 driving checks, and 5/5 guided visual checkpoints. Keep the
completed working demo separate when distributing the student exercise.
Upload it to Google Colab and save a copy in Google Drive, or open it locally
in Jupyter. It needs no packages, camera, or hardware. Run the cells in order.

Students use a mock `car.scan()` interface and complete `control_step()` in one
student code cell with numbered checkpoint comments. The debug cell directly
below checks pedestrian, stop-sign, distance, unexpected-reading, and clear-road
scenarios and points students back to the relevant checkpoint. After each edit,
run the student cell and then the debug cell. The mock setup cell is collapsed in Colab. Camera detection
and PyTorch implementation code are not included. The checks give specific hints;
they are practice feedback, not the full simulator's driving score. Copy the
student controller function into the full controller when ready; the route still requires
steering, obstacle avoidance, and stop-sign timing.

Checkpoint 7 adds personal choices in that same student cell: a driver name,
a custom obstacle label, and a left/right detour preference. Debug checks test
the chosen steering, straightening after the object clears, and stopping if it
is too close. These are mock decision checks, not a geometric avoidance test.
A custom label does not train the real detector. It is illustrated in the
guided replay but does not add a new object to the advanced full simulator. Keep the custom settings with any controller that uses them.

The debug cell runs a short, guided HTML skills course using the same student
function: move, yield to a crossing person, stop at a sign, stop before a box,
and steer around a personal object. The course supplies position-based mock observations;
it is not a vehicle physics or full-route navigation test. The pedestrian starts crossing as the car approaches. A fixed roadside sign
and painted stop line stay in place after the wait. A worker visibly pushes the
box to the shoulder after the car stops; neither vanishes. The custom object
stays fixed while the car follows a smooth guided detour. All five scene objects
persist throughout the replay. Correct custom steering triggers the guided curve.
The course ends immediately on a wrong action or steering choice and gives a hint.
No waypoints, coordinates, stop timers, or route planning are required.

The notebook follows the existing Weeks 1–6 materials, especially the Week 3–5
read/predict/run/change/explain routine. Sensor-reading lines are provided as a
worked starting point. An instructor example connects a familiar string comparison
to a car action. Students implement short conditions inside the supplied function;
the runner supplies repetition. Dictionary state and class construction are not
required. The notebook maps these tasks back to the earlier lessons without
assuming that exposure to a concept means mastery.

The notebook includes a three-hour plan: 15 minutes for arrival/setup, a short
demonstration, checkpoint work, two ten-minute breaks, personalization, replay,
and submission. The target is eight mock checks plus five guided skills
checkpoints. The advanced strict cul-de-sac remains available separately through
`run_student.py` and `picarx-driving-challenge.ipynb`.

The replay is bundled for Colab and saves to
`picarx_notebook/camera_skills_replay.html` in the notebook runtime. Download it
from Colab's Files panel if the embedded viewer is unavailable.

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

In the starter's type hints, `car: CoursePicarx` means the simulator hands
you a virtual car with methods such as `forward()` and `stop()`.
`memory: dict[str, object]` means you use string keys and can store different
kinds of values, such as a Boolean or a number. The simulator keeps that
dictionary between calls. `-> None` means your function has no value to
return. Calling a car method is how you tell it what to do.

## Student-facing API

| Command or sensor | Meaning |
| --- | --- |
| `car.forward(speed)` | Move forward at a speed from 0 to 100. |
| `car.backward(speed)` | Move backward at a speed from 0 to 100. |
| `car.stop()` | Stop both drive motors. |
| `car.set_dir_servo_angle(angle)` | Steer from -30 degrees to +30 degrees. |
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
def control_step(car: CoursePicarx, memory: dict[str, object]) -> None:
    scan_input: str = car.scan()

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

### Class 1 â€” Safe baseline

- Inspect the simulator and connect the API to the physical PiCar-X vocabulary.
- Write a controller that starts, steers, stops, and avoids one obstacle.
- Use the practice replay to explain one decision made by the program.
- Commit a working baseline.

### Class 2 â€” Reliability and competition

- Test slalom, tight-turn, and sensor-fault scenarios.
- Add helper functions and a `memory` state.
- Compare scores without copying code.
- Record one failure, its cause, and the change that fixed it.

### Class 3 â€” Validation and showcase

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

## Simulation and hardware share a base class

The inheritance chain is SunFounder's Picarx, then CoursePicarx, then
VirtualPicarx or HardwarePicarx. The pinned SunFounder source and license
are in vendor/. HardwarePicarx inherits the real steering, motor, calibration,
and sensor implementation. VirtualPicarx replaces those operations with
simulation behavior and uses the same steering limits of -30 to +30 degrees.

Student controllers import CoursePicarx from car_api for their type hints.
Keep decision logic within the documented course API. Vendor calibration
and low-level motor configuration methods are intended for hardware setup.

The camera scan and turn_left/turn_right helpers are course additions.
HardwarePicarx uses CameraScanner from camera_scanner.py. A COCO-trained
YOLO11 nano model detects people and stop signs in camera frames. A person
overlapping the middle 70% of the image with feet below the top quarter
is treated as potentially in the car's path. Human detections take priority.
The scanner holds a human label for 0.8 seconds and a sign label for
0.4 seconds after the last qualifying detection to reduce flicker.
These are starting thresholds to tune against the real course.

On a configured Raspberry Pi, install SunFounder's robot_hat dependencies
using its official hardware setup instructions. The simulation and Colab
do not need those packages. For the default Pi camera, run:

    .camera-venv/bin/python run_hardware.py --seconds 30

The hardware runner calls the same student_controller.control_step at a
target interval of 0.12 seconds and stops the motors when the run exits.
Ten stopped steps are nominally 1.2 seconds. Detection latency can change
real timing, so camera thresholds, stop location, steering and sensor
calibration still require physical-course validation. Simulation scores
demonstrate behavior within this model.

Source and installation instructions:
https://github.com/sunfounder/picar-x/tree/2.1.x

## Camera setup and bench testing

Run `python setup_camera.py` once with internet access. It creates
`.camera-venv`, installs the camera requirements, and downloads
`yolo11n.pt`. On Raspberry Pi OS, install Picamera2 first with
`sudo apt install python3-picamera2`. The virtual environment includes
system packages so it can use Picamera2 and robot_hat installed on the Pi.
USB cameras use OpenCV and can also be tested on a laptop.

Before connecting driving commands, test a photo and the camera:

    .camera-venv/bin/python camera_scanner.py --image photo.jpg
    .camera-venv/bin/python camera_scanner.py --camera picamera2
    .camera-venv/bin/python camera_scanner.py --camera usb --camera-index 0

On Windows setup uses `%USERPROFILE%\.venvs\picarx-camera\Scripts\python.exe`
to avoid long package installation paths.
Image mode prints the chosen label plus bounding boxes and confidence scores.
Camera mode prints labels and scan latency without starting the motors.

The concrete perception methods are `read_frame()`, `detect_frame(frame)`,
`select_label(detections, now)`, and `scan()`. Students continue calling
`car.scan()`. HardwarePicarx stops the motors before synchronous scanning,
so slow inference leaves the car stopped. Capture/model errors propagate to
the hardware runner, which also stops the car in its cleanup block.
A completed scan taking over two seconds raises an error. This check runs
after capture and inference return and cannot interrupt a blocked camera call.

Stop-sign bounding-box area is an approach heuristic, not a distance reading.
The default minimum is 0.5% of the image. Use
`--minimum-sign-area` and `--confidence` in the bench tool to inspect thresholds.
Printed toy-scale signs, small figures, occlusion, motion blur and lighting
need real-course tests and potentially model fine-tuning. A person leaving
the image can also be a camera blind spot, so the dropout hold alone does
not establish that a crossing is clear. Boxes still use ultrasonic readings.

Detector API and camera color-order references:
https://docs.ultralytics.com/modes/predict/
https://github.com/raspberrypi/picamera2/blob/main/picamera2/request.py
