"""Continuous, fixed-world skills course behind the beginner camera interface.

The camera is mocked. The custom detour uses a guided lane-change curve,
not a vehicle dynamics model. Students only supply sensor/action decisions.
"""
import math


def run_guided_course(controller, obstacle, direction, car_factory):
    from simulator import Scenario, Checkpoint, RunResult, SceneObject

    if direction not in ("left", "right"):
        raise ValueError("Choose left or right.")
    if not isinstance(obstacle, str) or not obstacle.strip() or obstacle in ("clear", "human", "stop sign", "unknown"):
        raise ValueError("Choose a new, nonempty personal-object label.")
    car = car_factory()
    memory = {}
    frames = []
    x, y, heading = 65.0, 260.0, 0.0
    traveled = 0.0
    sign_wait = 0
    sign_done = False
    crossing_start = None
    box_wait = 0
    box_move_start = None
    failure = ""
    completed = 0
    changes = 0
    previous_angle = 0
    side = -1 if direction == "left" else 1
    checkpoint_x = (150, 340, 550, 850, 1450)
    scene = (
        SceneObject("human", 300, 165, 12, (300, 355)),
        SceneObject("stop sign", 480, 355, 18),
        SceneObject("box", 760, 260, 18),
        SceneObject(obstacle, 1110, 260, 18),
        SceneObject("human", 785, 390, 12),
    )
    for tick in range(2200):
        if x >= 175 and crossing_start is None:
            crossing_start = tick
        crossing = min(1.0, (tick - crossing_start) / 100) if crossing_start is not None else 0.0
        person_y = 165 + 190 * crossing
        box_progress = min(1.0, (tick-box_move_start)/70) if box_move_start is not None else 0.0
        box_y = 260 + 130 * box_progress
        worker_y = box_y + 35
        person_in_path = crossing_start is not None and crossing < 1 and 300-x < 105
        worker_in_path = box_move_start is not None and worker_y < 325
        custom_in_view = 960 <= x < 1260
        distance_cm = 200.0
        for bx, by in ((760, box_y), (1110, 260)):
            if bx > x and abs(by-y) < 30:
                distance_cm = min(distance_cm, max(0, bx-x-18))
        if person_in_path or worker_in_path:
            label = "human"
        elif 400 <= x < 500 and not sign_done:
            label = "stop sign"
        elif custom_in_view:
            label = obstacle
        else:
            label = "clear"
        car.label, car.distance, car.history = label, distance_cm, []
        try:
            controller(car, memory)
        except Exception as error:
            failure = f"Controller error: {type(error).__name__}: {error}"
        speed = car.history[-1][1] if car.history and car.action == "forward" else 0
        moving = speed > 0
        issued_forward = any(action == "forward" for action, power in car.history)
        must_stop = label in ("human", "stop sign") or distance_cm < 25
        if not failure and must_stop and (moving or issued_forward):
            failure = ("Yield to the pedestrian" if label == "human" else
                       "Stop at the sign" if label == "stop sign" else
                       "Stop before the nearby box")
        if not failure and moving and label == obstacle and car.steering != side*25:
            failure = f"Steer {direction} around {obstacle}: use angle {side*25}."
        if not failure and moving and label == "clear" and car.steering != 0:
            failure = "Straighten the wheels when the view clears."
        if label == "stop sign" and not moving and not failure:
            sign_wait += 1
            sign_done = sign_wait >= 12
        if 690 <= x < 760 and distance_cm < 25 and not moving and not failure:
            box_wait += 1
            if box_wait >= 8 and box_move_start is None:
                box_move_start = tick
        if not failure and moving:
            previous_x, previous_y = x, y
            x += speed * 0.72 * 0.12
            # The course adapter guides the lane change; no path math in student code.
            t = max(0.0, min(1.0, (x-960)/300))
            y = 260 + side * 70 * math.sin(math.pi*t)**2
            heading = math.degrees(math.atan(side*70*math.pi/300*math.sin(2*math.pi*t)))
            traveled += math.hypot(x-previous_x, y-previous_y)
            if x >= 455 and not sign_done:
                failure = "Ran the stop sign"
            for bx, by in ((760, box_y), (1110,260)):
                if math.hypot(x-bx,y-by) < 30:
                    failure = "Hit an obstacle"
            if math.hypot(x-300,y-person_y) < 24:
                failure = "Hit a pedestrian"
        completed = sum(x >= point for point in checkpoint_x)
        objects = [
            dict(id="crossing-person",kind="human",x=300,y=person_y,radius=12,walking=0<crossing<1),
            dict(id="roadside-sign",kind="stop sign",x=480,y=355,radius=18,walking=False),
            dict(id="movable-box",kind="box",x=760,y=box_y,radius=18,walking=False),
            dict(id="personal-object",kind=obstacle,x=1110,y=260,radius=18,walking=False),
            dict(id="worker",kind="human",x=785,y=worker_y,radius=12,walking=0<box_progress<1),
        ]
        changes += car.steering != previous_angle
        previous_angle = car.steering
        frames.append(dict(step=tick,x=round(x,2),y=round(y,2),heading=round(heading,2),
            steering=car.steering,throttle=0 if failure else speed,checkpoint=completed,
            scan=label,objects=objects,failure=failure))
        if completed == 5 or failure:
            break
        if len(frames)>240 and math.hypot(x-frames[-240]["x"], y-frames[-240]["y"])<2:
            failure = "No progress: check for an unconditional stop or an early return."
            frames[-1]["failure"] = failure
            break
    else:
        failure = "Course time limit reached. Use forward(30) when the road is clear."
        frames[-1]["failure"] = failure
    success = completed == 5 and not failure
    frames[-1]["throttle"] = 0
    scenario = Scenario("guided_neighborhood",1600,520,(65,260,0),Checkpoint(1450,260,32),(),
        tuple(Checkpoint(cx,260,32) for cx in checkpoint_x),((40,260),(1550,260)),scene,
        max_steps=2200)
    # Keep compatibility with earlier Scenario constructors used in Colab.
    object.__setattr__(scenario, "road_half_width", 85)
    result = RunResult(scenario=scenario.name,reached_goal=success,checkpoints_reached=completed,
        total_checkpoints=5,collisions=int(failure=="Hit an obstacle"),boundary_hits=0,
        invalid_commands=0,sensor_faults_seen=0,steps=len(frames),distance_traveled=round(traveled,2),
        steering_changes=changes,stopped_safely=True,human_hits=int(failure=="Hit a pedestrian"),
        stop_sign_violations=int(failure=="Ran the stop sign"),stop_signs_obeyed=int(sign_done),replay=frames)
    print(f"Skills checkpoints: {completed}/5")
    if failure:
        print("TRY AGAIN:",failure)
    return result, scenario
