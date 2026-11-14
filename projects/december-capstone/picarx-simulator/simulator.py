"""Deterministic, standard-library-only PiCar-X navigation simulator."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
import json
import math
import random
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Circle:
    x: float
    y: float
    radius: float


@dataclass(frozen=True)
class Checkpoint:
    x: float
    y: float
    radius: float = 38


@dataclass(frozen=True)
class SceneObject:
    """An object that can be recognized by the virtual camera."""

    kind: str
    x: float
    y: float
    radius: float = 18
    crossing_end: tuple[float, float] | None = None


@dataclass(frozen=True)
class Scenario:
    name: str
    width: int
    height: int
    start: tuple[float, float, float]
    goal: Checkpoint
    obstacles: tuple[Circle, ...]
    checkpoints: tuple[Checkpoint, ...] = ()
    route: tuple[tuple[float, float], ...] = ()
    scene_objects: tuple[SceneObject, ...] = ()
    max_steps: int = 650
    sensor_fault_every: int = 0
    seed: int = 1
    branches: tuple[tuple[tuple[float, float], ...], ...] = ()
    turning_bulb: tuple[float, float, float] | None = None

    def road_segments(self):
        for road in (self.route, *self.branches):
            yield from zip(road, road[1:])


@dataclass
class RunResult:
    scenario: str
    reached_goal: bool
    checkpoints_reached: int
    total_checkpoints: int
    collisions: int
    boundary_hits: int
    invalid_commands: int
    sensor_faults_seen: int
    steps: int
    distance_traveled: float
    steering_changes: int
    stopped_safely: bool
    human_hits: int = 0
    stop_sign_violations: int = 0
    stop_signs_obeyed: int = 0
    controller_errors: list[str] = field(default_factory=list)
    replay: list[dict] = field(default_factory=list)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def point_to_segment(point: tuple[float, float], start: tuple[float, float], end: tuple[float, float]) -> float:
    """Shortest distance between a point and one route-line segment."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    if dx == 0 and dy == 0:
        return distance(point, start)
    amount = clamp(((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / (dx * dx + dy * dy), 0, 1)
    projection = (start[0] + amount * dx, start[1] + amount * dy)
    return distance(point, projection)


class VirtualUltrasonic:
    def __init__(self, car: "VirtualPicarx") -> None:
        self.car = car

    def read(self) -> float:
        """Return virtual centimeters to an obstacle or -1 for a sensor fault."""
        self.car.sensor_reads += 1
        fault_every = self.car.scenario.sensor_fault_every
        if fault_every and self.car.sensor_reads % fault_every == 0:
            self.car.sensor_faults_seen += 1
            return -1.0

        heading = math.radians(self.car.heading)
        for ray_distance in range(2, 201, 2):
            x = self.car.x + math.cos(heading) * ray_distance
            y = self.car.y + math.sin(heading) * ray_distance
            if not (0 <= x <= self.car.scenario.width and 0 <= y <= self.car.scenario.height):
                return float(ray_distance)
            if any(distance((x, y), (item.x, item.y)) <= item.radius for item in self.car.scenario.obstacles):
                return float(ray_distance)
        return 200.0


class VirtualPicarx:
    """Small compatibility layer modeled after SunFounder's Picarx API."""

    is_simulation = True

    def __init__(self, scenario: Scenario) -> None:
        self.scenario = scenario
        self.x, self.y, self.heading = scenario.start
        self.throttle = 0.0
        self.steering = 0.0
        self.ultrasonic = VirtualUltrasonic(self)
        self.invalid_commands = 0
        self.sensor_reads = 0
        self.sensor_faults_seen = 0
        self.last_scan = "clear"
        self.scene_objects = scenario.scene_objects
        self.crossing_people: set[int] = set()

    def _number(self, value: object, default: float = 0.0) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            self.invalid_commands += 1
            return default
        return float(value)

    def forward(self, speed: float) -> None:
        speed = self._number(speed)
        if not 0 <= speed <= 100:
            self.invalid_commands += 1
        self.throttle = clamp(speed, 0, 100)

    def backward(self, speed: float) -> None:
        speed = self._number(speed)
        if not 0 <= speed <= 100:
            self.invalid_commands += 1
        self.throttle = -clamp(speed, 0, 100)

    def stop(self) -> None:
        self.throttle = 0.0

    def turn_left(self, speed: float = 28) -> None:
        """Begin a readable left turn using the real steering and motor calls."""
        self.set_dir_servo_angle(-28)
        self.forward(speed)

    def turn_right(self, speed: float = 28) -> None:
        """Begin a readable right turn using the real steering and motor calls."""
        self.set_dir_servo_angle(28)
        self.forward(speed)

    def set_dir_servo_angle(self, angle: float) -> None:
        angle = self._number(angle)
        if not -35 <= angle <= 35:
            self.invalid_commands += 1
        self.steering = clamp(angle, -35, 35)

    def set_cam_pan_angle(self, angle: float) -> None:
        self._number(angle)

    def set_cam_tilt_angle(self, angle: float) -> None:
        self._number(angle)

    def get_grayscale_data(self) -> list[int]:
        """Return left/center/right ground brightness readings.

        A low value means the sensor is over the dark route line, matching the
        physical lesson's left/center/right grayscale list.
        """
        readings: list[int] = []
        heading = math.radians(self.heading)
        for side_offset in (-18, 0, 18):
            sensor_x = self.x + math.cos(heading) * 16 + math.cos(heading + math.pi / 2) * side_offset
            sensor_y = self.y + math.sin(heading) * 16 + math.sin(heading + math.pi / 2) * side_offset
            route_distance = min(
                point_to_segment((sensor_x, sensor_y), start, end)
                for start, end in self.scenario.road_segments()
            )
            readings.append(250 if route_distance <= 11 else 1200)
        return readings

    def scan(self) -> str:
        """Return the closest camera-recognized object or ``clear``.

        This intentionally hides computer-vision math from beginners. In a
        physical build, a camera model would supply the same small vocabulary.
        """
        heading = math.radians(self.heading)
        visible: list[tuple[float, str]] = []
        for index, item in enumerate(self.scene_objects):
            if index in self.crossing_people:
                visible.append((0, "human"))
                continue
            if item.crossing_end is not None:
                continue
            dx, dy = item.x - self.x, item.y - self.y
            forward = dx * math.cos(heading) + dy * math.sin(heading)
            sideways = -dx * math.sin(heading) + dy * math.cos(heading)
            # A stop sign is reported only after the car enters the legal
            # stopping zone. This keeps recognition and scoring synchronized.
            recognition_range = 68 if item.kind == "stop sign" else 145
            if 0 < forward <= recognition_range and abs(math.degrees(math.atan2(sideways, forward))) <= 38:
                visible.append((math.hypot(dx, dy), item.kind))
        self.last_scan = min(visible)[1] if visible else "clear"
        return self.last_scan

    def step(self, seconds: float = 0.12) -> tuple[float, float, float]:
        previous = (self.x, self.y)
        speed = self.throttle * 0.72
        turn_rate = speed * math.tan(math.radians(self.steering)) / 38
        self.heading = (self.heading + math.degrees(turn_rate * seconds)) % 360
        heading = math.radians(self.heading)
        self.x += math.cos(heading) * speed * seconds
        self.y += math.sin(heading) * speed * seconds
        return previous[0], previous[1], distance(previous, (self.x, self.y))


def scenario_catalog() -> dict[str, Scenario]:
    practice = Scenario(
        "practice", 900, 520, (65, 260, 29), Checkpoint(835, 260, 42),
        (Circle(350, 235, 38), Circle(610, 220, 32)),
        (Checkpoint(230, 350), Checkpoint(490, 350), Checkpoint(720, 225)),
        ((65, 260), (230, 350), (490, 350), (720, 225), (835, 260)),
        (SceneObject("stop sign", 159, 352),
         SceneObject("human", 687, 307, 12, (639, 219))), max_steps=700,
    )
    slalom = Scenario(
        "slalom", 900, 520, (65, 260, 0), Checkpoint(835, 260, 42),
        (Circle(260, 250, 38), Circle(445, 280, 38), Circle(620, 250, 38), Circle(735, 310, 34)),
        (Checkpoint(300, 375), Checkpoint(500, 130), Checkpoint(680, 385)),
        ((65, 260), (300, 375), (500, 130), (680, 385), (835, 260)),
        (SceneObject("human", 275, 355), SceneObject("stop sign", 445, 115), SceneObject("human", 705, 350)), max_steps=850,
    )
    tight_turn = Scenario(
        "tight_turn", 760, 620, (70, 520, 270), Checkpoint(680, 90, 42),
        (Circle(190, 390, 48), Circle(380, 300, 52), Circle(570, 210, 48)),
        (Checkpoint(100, 260), Checkpoint(310, 100), Checkpoint(520, 430)),
        ((70, 520), (100, 260), (310, 100), (520, 430), (680, 90)),
        (SceneObject("stop sign", 55, 275), SceneObject("human", 505, 410)), max_steps=900,
    )
    sensor_fault = Scenario(
        "sensor_fault", 900, 520, (65, 260, 0), Checkpoint(835, 260, 42),
        (Circle(350, 250, 38), Circle(600, 315, 38)),
        (Checkpoint(250, 150), Checkpoint(520, 150), Checkpoint(730, 250)),
        ((65, 260), (250, 150), (520, 150), (730, 250), (835, 260)),
        (SceneObject("human", 500, 145), SceneObject("stop sign", 700, 205)),
        max_steps=800, sensor_fault_every=9,
    )
    rng = random.Random(271828)
    unseen_obstacles = tuple(Circle(rng.randint(230, 700), rng.randint(120, 400), rng.randint(34, 55)) for _ in range(4))
    unseen = Scenario(
        "unseen", 900, 520, (65, 260, 0), Checkpoint(835, 260, 42), unseen_obstacles,
        (Checkpoint(300, 95), Checkpoint(500, 430), Checkpoint(710, 95)),
        ((65, 260), (300, 95), (500, 430), (710, 95), (835, 260)),
        (SceneObject("stop sign", 255, 75), SceneObject("human", 520, 405)), max_steps=900, seed=271828,
    )
    warehouse = replace(
        practice, name="warehouse", width=1740, height=920, max_steps=2000,
        route=(*practice.route, (960, 285), (1130, 365), (1280, 440)),
        turning_bulb=(1330, 440, 305),
        goal=Checkpoint(915, 302, 42),
        checkpoints=(*practice.checkpoints, Checkpoint(980, 285, 52),
                     Checkpoint(1115, 315, 54), Checkpoint(1255, 223, 58),
                     Checkpoint(1450, 237, 58), Checkpoint(1540, 420, 58),
                     Checkpoint(1460, 625, 58), Checkpoint(1240, 640, 58),
                     Checkpoint(1115, 490, 54)),
        obstacles=(*practice.obstacles, Circle(1015, 315, 27), Circle(1190, 285, 33),
                   Circle(1320, 215, 30), Circle(1440, 349, 37),
                   Circle(1510, 520, 32), Circle(1345, 620, 35),
                   Circle(1205, 535, 30), Circle(1280, 430, 39)),
    )
    warehouse_alt = replace(
        warehouse, name="warehouse_alt",
        obstacles=(*practice.obstacles, Circle(1015, 262, 27), Circle(1190, 385, 33),
                   Circle(1350, 270, 32), Circle(1485, 330, 37),
                   Circle(1490, 552, 32), Circle(1335, 575, 39),
                   Circle(1160, 510, 30), Circle(1280, 430, 39)),
    )
    return {item.name: item for item in
            (practice, slalom, tight_turn, sensor_fault, unseen, warehouse, warehouse_alt)}


def run_scenario(controller: Callable, scenario: Scenario, *, strict: bool = False) -> RunResult:
    car = VirtualPicarx(scenario)
    memory: dict = {}
    replay: list[dict] = []
    collisions = boundary_hits = steering_changes = 0
    was_in_collision = was_outside = False
    distance_traveled = 0.0
    checkpoint_index = 0
    previous_steering = car.steering
    errors: list[str] = []
    reached_goal = False
    human_hits = 0
    stop_sign_violations = 0
    stop_signs_obeyed = 0
    human_contacts: set[int] = set()
    completed_signs: set[int] = set()
    sign_stop_counts: dict[int, int] = {}

    crossing_starts: dict[int, int] = {}
    stop_lines = {}
    for index, item in enumerate(scenario.scene_objects):
        if item.kind != "stop sign" or len(scenario.route) < 2:
            continue
        start, end = min(scenario.road_segments(),
                         key=lambda segment: point_to_segment((item.x, item.y), *segment))
        length = distance(start, end)
        if length:
            dx, dy = (end[0] - start[0]) / length, (end[1] - start[1]) / length
            along = clamp((item.x - start[0]) * dx + (item.y - start[1]) * dy, 0, length)
            stop_lines[index] = (start[0] + along * dx, start[1] + along * dy, dx, dy)

    for step_number in range(scenario.max_steps):
        people = list(scenario.scene_objects)
        car.crossing_people.clear()
        for index, item in enumerate(people):
            if item.crossing_end is None:
                continue
            end_x, end_y = item.crossing_end
            midpoint = ((item.x + end_x) / 2, (item.y + end_y) / 2)
            if distance((car.x, car.y), midpoint) <= 94:
                crossing_starts.setdefault(index, step_number)
            if index in crossing_starts:
                progress = min(1, (step_number - crossing_starts[index]) / 36)
                people[index] = replace(item, x=item.x + (end_x - item.x) * progress,
                                        y=item.y + (end_y - item.y) * progress)
                # Let the pedestrian approach the lane before the controller yields.
                if 0.22 <= progress < 1:
                    car.crossing_people.add(index)
        car.scene_objects = tuple(people)
        try:
            controller(car, memory)
        except Exception as error:  # Student errors become feedback instead of crashing the evaluator.
            errors.append(f"Step {step_number}: {type(error).__name__}: {error}")
            car.stop()
            break

        if abs(car.steering - previous_steering) >= 8:
            steering_changes += 1
        previous_steering = car.steering
        old_x, old_y, moved = car.step()
        distance_traveled += moved

        outside = not (12 <= car.x <= scenario.width - 12 and 12 <= car.y <= scenario.height - 12)
        hit = any(distance((car.x, car.y), (item.x, item.y)) <= item.radius + 12 for item in scenario.obstacles)
        if outside or hit:
            if outside and not was_outside:
                boundary_hits += 1
            if hit and not was_in_collision:
                collisions += 1
            car.x, car.y = old_x, old_y
            car.throttle = 0
        was_outside = outside
        was_in_collision = hit

        for object_index, item in enumerate(car.scene_objects):
            object_distance = distance((car.x, car.y), (item.x, item.y))
            if item.kind == "human" and object_distance <= item.radius + 12 and object_index not in human_contacts:
                human_hits += 1
                human_contacts.add(object_index)
                car.x, car.y = old_x, old_y
                car.stop()
                break
            if item.kind == "stop sign" and object_index not in completed_signs:
                # Recognition defines the approach zone. Counting the same
                # signal here prevents visual stopping and scoring from drifting.
                line = stop_lines.get(object_index)
                crossed = False
                in_stop_zone = object_distance <= 72
                if line:
                    line_x, line_y, dx, dy = line
                    before = (old_x - line_x) * dx + (old_y - line_y) * dy
                    after = (car.x - line_x) * dx + (car.y - line_y) * dy
                    lateral = abs((car.y - line_y) * dx - (car.x - line_x) * dy)
                    crossed = before < 0 <= after and lateral <= 35
                    in_stop_zone = -68 <= after <= 0 and lateral <= 35
                if in_stop_zone and moved == 0:
                    sign_stop_counts[object_index] = sign_stop_counts.get(object_index, 0) + 1
                    if sign_stop_counts[object_index] >= 10:
                        stop_signs_obeyed += 1
                        completed_signs.add(object_index)
                else:
                    sign_stop_counts[object_index] = 0
                if crossed and object_index not in completed_signs:
                    stop_sign_violations += 1
                    car.stop()
                    break

        failure = ""
        if human_hits:
            failure = "Hit a pedestrian"
        elif stop_sign_violations:
            failure = "Ran the stop sign"
        elif strict and hit:
            failure = "Hit a box"
        elif strict and outside:
            failure = "Crossed the course boundary"
        elif strict and len(replay) >= 120:
            # Allow traffic waits and brief recovery, but end a stuck loop.
            earlier = replay[-120]
            if (earlier["checkpoint"] == checkpoint_index
                    and distance((car.x, car.y), (earlier["x"], earlier["y"])) < 12):
                failure = "Stalled without making progress"
        safety_failure = bool(failure)
        if safety_failure:
            car.stop()
        if not safety_failure and checkpoint_index < len(scenario.checkpoints):
            point = scenario.checkpoints[checkpoint_index]
            if distance((car.x, car.y), (point.x, point.y)) <= point.radius:
                checkpoint_index += 1

        if not safety_failure and checkpoint_index == len(scenario.checkpoints) and distance((car.x, car.y), (scenario.goal.x, scenario.goal.y)) <= scenario.goal.radius:
            reached_goal = True
            car.stop()

        replay.append({
            "step": step_number, "x": round(car.x, 2), "y": round(car.y, 2),
            "heading": round(car.heading, 2), "steering": round(car.steering, 2),
            "throttle": round(car.throttle, 2), "checkpoint": checkpoint_index,
            "scan": car.last_scan,
            "objects": [
                {**item.__dict__, "walking": index in crossing_starts
                 and step_number < crossing_starts[index] + 36}
                for index, item in enumerate(car.scene_objects)
            ],
            "failure": failure,
        })
        if reached_goal or safety_failure:
            break

    return RunResult(
        scenario.name, reached_goal, checkpoint_index, len(scenario.checkpoints), collisions,
        boundary_hits, car.invalid_commands, car.sensor_faults_seen, len(replay),
        round(distance_traveled, 2), steering_changes, abs(car.throttle) < 0.01,
        human_hits, stop_sign_violations, stop_signs_obeyed, errors, replay,
    )


def render_replay(result: RunResult, scenario: Scenario, output: Path) -> None:
    render_replays([(result, scenario)], output)


def render_replays(runs: list[tuple[RunResult, Scenario]], output: Path) -> None:
    payload = json.dumps([{
        "result": {key: value for key, value in result.__dict__.items() if key != "replay"},
        "frames": result.replay,
        "scenario": {
            "name": scenario.name, "width": scenario.width, "height": scenario.height,
            "goal": scenario.goal.__dict__,
            "obstacles": [item.__dict__ for item in scenario.obstacles],
            "checkpoints": [item.__dict__ for item in scenario.checkpoints],
            "route": scenario.route,
            "branches": scenario.branches,
            "turningBulb": scenario.turning_bulb,
            "sceneObjects": [item.__dict__ for item in scenario.scene_objects],
        },
    } for result, scenario in runs]).replace("<", "\\u003c")
    template = """<!doctype html><html><head><meta charset="utf-8"><title>Virtual PiCar-X Replay</title>
<style>body{font-family:Arial;background:#071b2e;color:white;margin:0;padding:22px}main{max-width:1100px;margin:auto}.card{background:#102d46;border:1px solid #2d6383;border-radius:14px;padding:16px;margin:12px 0}.views{display:grid;grid-template-columns:2fr 1fr;gap:14px}canvas{width:100%;background:#d9f0df;border-radius:10px}button,input{font-size:16px;margin-right:10px}strong{color:#55d6be}.legend span{margin-right:18px}@media(max-width:800px){.views{grid-template-columns:1fr}}</style></head>
<body><main><h1>Virtual PiCar-X Chase View</h1><div class="card" id="summary"></div><div class="views"><canvas id="driver" width="760" height="470"></canvas><canvas id="course"></canvas></div>
<div class="card"><button id="play">Play</button><button id="reset">Reset</button><input id="slider" type="range" min="0" value="0"><span id="step"></span> · <strong id="score"></strong></div>
<p class="card" id="hint" role="status" hidden></p>
<div class="legend"><span>🟦 Car</span><span>🟥 Obstacle</span><span>🟨 Checkpoint</span><span>🟩 Goal</span></div></main>
<script>const runs=__DATA__,c=document.querySelector('#course'),x=c.getContext('2d'),d=document.querySelector('#driver'),v=d.getContext('2d');
const slider=document.querySelector('#slider');
const playButton=document.querySelector('#play');
const selector=document.createElement('select');
selector.setAttribute('aria-label','Course');
playButton.before(selector);
selector.hidden=runs.length===1;
runs.forEach((run,index)=>selector.add(new Option(run.scenario.name.replaceAll('_',' '),index)));
let data,s,roads,i=0,t=null;
function selectCourse(){
    pause();
    data=runs[Number(selector.value)];
    s=data.scenario;
    roads=[s.route,...s.branches].filter(route=>route.length>=2).map(routeSamples);
    c.width=s.width;
    c.height=s.height;
    i=0;
    slider.value=0;
    slider.max=Math.max(0,data.frames.length-1);
    playButton.disabled=!data.frames.length;
    const result=data.result;
    document.querySelector('#summary').textContent=
        `${s.name} | Goal: ${result.reached_goal?'reached':'not reached'} | Checkpoints: ${result.checkpoints_reached}/${result.total_checkpoints} | Collisions: ${result.collisions}`;
    document.querySelector('#step').textContent=result.controller_errors[0]??'';
    showScore(0, !data.frames.length);
    showHint(0, !data.frames.length);
    d.getContext('2d').clearRect(0,0,d.width,d.height);
    draw();
}
function circle(o,color){x.beginPath();x.arc(o.x,o.y,o.radius,0,Math.PI*2);x.fillStyle=color;x.fill();}
function worldToCamera(o,f){const a=f.heading*Math.PI/180,dx=o.x-f.x,dy=o.y-f.y;return{depth:dx*Math.cos(a)+dy*Math.sin(a),side:-dx*Math.sin(a)+dy*Math.cos(a)}}
function smoothstep(a,b,value){const t=Math.max(0,Math.min(1,(value-a)/(b-a)));return t*t*(3-2*t)}
function routeSamples(route){const pts=[];for(let n=0;n<route.length-1;n++){const a=route[n],b=route[n+1],length=Math.hypot(b[0]-a[0],b[1]-a[1]),steps=Math.max(2,Math.ceil(length/18));for(let k=0;k<steps;k++){const t=k/steps;pts.push({x:a[0]+(b[0]-a[0])*t,y:a[1]+(b[1]-a[1])*t})}}const z=route[route.length-1];pts.push({x:z[0],y:z[1]});return pts}
function perspective(point){
    const scale=340/point.depth;
    return {x:d.width/2+point.side*scale,y:155+55*scale,depth:point.depth,approach:Math.min(1,70/point.depth)};
}
function projectGround(point,frame){
    const camera=worldToCamera(point,frame);
    return camera.depth>=12 ? perspective(camera) : null;
}
function roadPolygon(points,frame,color){
    const camera=points.map(point=>worldToCamera(point,frame));
    const clipped=[];
    for(let index=0;index<camera.length;index++){
        const a=camera[index],b=camera[(index+1)%camera.length];
        if(a.depth>=12)clipped.push(a);
        if((a.depth>=12)!==(b.depth>=12)){
            const fraction=(12-a.depth)/(b.depth-a.depth);
            clipped.push({depth:12,side:a.side+(b.side-a.side)*fraction});
        }
    }
    if(clipped.length<3)return;
    v.beginPath();
    clipped.map(perspective).forEach((point,index)=>index?v.lineTo(point.x,point.y):v.moveTo(point.x,point.y));
    v.closePath();
    v.fillStyle=color;
    v.fill();
}
function roadEdge(sampledRoute,index,offset){
    const point=sampledRoute[index];
    const before=sampledRoute[Math.max(0,index-1)],after=sampledRoute[Math.min(index+1,sampledRoute.length-1)];
    const dx=after.x-before.x,dy=after.y-before.y,length=Math.hypot(dx,dy)||1;
    return {x:point.x-dy/length*offset,y:point.y+dx/length*offset};
}
function drawRoad(frame){
    for(const sampledRoute of roads)drawRoadStrip(frame,sampledRoute);
    if(s.turningBulb){
        const [x,y,radius]=s.turningBulb;
        const rim=Array.from({length:64},(_,index)=>{
            const angle=index*Math.PI/32;
            return {x:x+radius*Math.cos(angle),y:y+radius*Math.sin(angle)};
        });
        roadPolygon(rim,frame,'#484b50');
    }
}
function drawRoadStrip(frame,sampledRoute){
    function strip(index,left,right,color){
        roadPolygon([roadEdge(sampledRoute,index,left),roadEdge(sampledRoute,index,right),
                     roadEdge(sampledRoute,index+1,right),roadEdge(sampledRoute,index+1,left)],frame,color);
    }
    for(let index=0;index<sampledRoute.length-1;index++){
        const halfWidth=s.turningBulb && sampledRoute[index].x>=835?82:24;
        strip(index,-halfWidth-5,halfWidth+5,'#aab1a6');
        strip(index,-halfWidth,halfWidth,'#484b50');
        if(halfWidth>24)continue;
        strip(index,-23,-22,'#ece8dc');
        strip(index,22,23,'#ece8dc');
        if(index%3!==2)strip(index,-.8,.8,'#e8dcaa');
    }
}
function drawCar(width,height){
    v.save();
    v.translate(width/2,height-70);
    v.fillStyle='rgba(0,0,0,.35)';
    v.beginPath();
    v.ellipse(0,28,72,15,0,0,Math.PI*2);
    v.fill();
    for(const [left,top,wide,tall] of [[-53,-35,18,30],[35,-35,18,30],[-65,3,23,36],[42,3,23,36]]){
        v.fillStyle='#111820';
        v.fillRect(left,top,wide,tall);
        v.fillStyle='#39434d';
        for(let tread=top+4;tread<top+tall;tread+=6)v.fillRect(left+2,tread,wide-4,2);
    }
    v.fillStyle='#273440';
    v.beginPath();
    v.moveTo(-45,30);v.lineTo(-34,-33);v.lineTo(34,-33);v.lineTo(45,30);
    v.closePath();v.fill();
    v.strokeStyle='#637381';v.lineWidth=2;v.stroke();
    v.fillStyle='#247451';v.fillRect(-24,-11,48,28);
    v.fillStyle='#17242e';v.fillRect(-10,-5,19,14);
    v.fillStyle='#b7c4ce';v.fillRect(-22,18,44,8);
    v.fillStyle='#718392';v.fillRect(-5,-53,10,34);
    v.fillStyle='#202a33';v.fillRect(-14,-62,28,16);
    v.fillStyle='#10181f';v.fillRect(-10,-59,20,10);
    v.fillStyle='#69c3e0';v.fillRect(-3,-56,6,4);
    v.restore();
}
function drawCrosswalk(camera){
    for(const person of s.sceneObjects){
        if(!person.crossing_end)continue;
        const dx=person.crossing_end[0]-person.x,dy=person.crossing_end[1]-person.y;
        const length=Math.hypot(dx,dy);
        if(!length)continue;
        const alongX=dy/length*5,alongY=-dx/length*5;
        for(let offset=.26;offset<.72;offset+=.105){
            const x=person.x+dx*offset,y=person.y+dy*offset;
            roadPolygon([
                {x:x-alongX,y:y-alongY},{x:x+alongX,y:y+alongY},
                {x:x+alongX+dx*.06,y:y+alongY+dy*.06},
                {x:x-alongX+dx*.06,y:y-alongY+dy*.06}
            ],camera,'#f4efe0');
        }
    }
}
function driverView(f){const W=d.width,H=d.height,h=155;let g=v.createLinearGradient(0,0,0,h);g.addColorStop(0,'#69b9e8');g.addColorStop(1,'#d9f4ff');v.fillStyle=g;v.fillRect(0,0,W,h);g=v.createLinearGradient(0,h,0,H);g.addColorStop(0,'#65a75f');g.addColorStop(1,'#254f2e');v.fillStyle=g;v.fillRect(0,h,W,H-h);for(let n=0;n<7;n++){const tx=35+n*118;v.fillStyle='#386b35';v.beginPath();v.arc(tx,h-8-(n%2)*12,18+(n%3)*5,0,Math.PI*2);v.fill();v.fillStyle='#79553a';v.fillRect(tx-3,h-2,6,28)}const angle=f.heading*Math.PI/180;const camera={...f,x:f.x-64*Math.cos(angle),y:f.y-64*Math.sin(angle)};drawRoad(camera);drawCrosswalk(camera);const objects=[...s.obstacles.map(o=>({...o,kind:'obstacle'})),...f.objects];objects.map(o=>({o,p:projectGround(o,camera)})).filter(q=>q.p&&q.p.depth<220&&Math.abs(q.p.x-W/2)<W*.65).sort((a,b)=>b.p.depth-a.p.depth).forEach(q=>{const scale=.3+q.p.approach*1.9,ground=q.p.y;const sx=q.p.x;const stride=q.o.walking?Math.sin(f.step*.48)*8:0;if(q.o.kind==='human'){v.strokeStyle='#f9c34e';v.lineWidth=Math.max(3,7*scale);v.beginPath();v.arc(sx,ground-45*scale,9*scale,0,Math.PI*2);v.moveTo(sx,ground-35*scale);v.lineTo(sx,ground-8*scale);v.moveTo(sx,ground-25*scale);v.lineTo(sx-14*scale,ground-15*scale);v.moveTo(sx,ground-25*scale);v.lineTo(sx+14*scale,ground-15*scale);v.moveTo(sx,ground-8*scale);v.lineTo(sx-12*scale,ground+(10+stride)*scale);v.moveTo(sx,ground-8*scale);v.lineTo(sx+12*scale,ground+10*scale);v.stroke()}else if(q.o.kind==='stop sign'){v.fillStyle='#70757b';v.fillRect(sx-2*scale,ground-38*scale,4*scale,43*scale);v.fillStyle='#c9252d';v.strokeStyle='white';v.lineWidth=Math.max(1,2*scale);v.beginPath();for(let n=0;n<8;n++){const a=Math.PI/8+n*Math.PI/4,px=sx+18*scale*Math.cos(a),py=ground-51*scale+18*scale*Math.sin(a);n?v.lineTo(px,py):v.moveTo(px,py)}v.closePath();v.fill();v.stroke();v.fillStyle='white';v.font=`bold ${Math.max(7,8*scale)}px Arial`;v.textAlign='center';v.fillText('STOP',sx,ground-48*scale)}else{drawBox(sx,ground,scale*q.o.radius/26)}});drawCar(W,H);v.fillStyle='rgba(4,15,27,.82)';v.fillRect(0,H-36,W,36);v.fillStyle='#55d6be';v.font='bold 18px Arial';v.textAlign='left';v.fillText(`${f.failure || (f.scan==='human' && !f.throttle ? 'YIELDING - PEDESTRIAN CROSSING' : '') || 'CAMERA: '+f.scan.toUpperCase()+'   SPEED: '+Math.abs(f.throttle).toFixed(0)}`,16,H-12)}
function drawBox(x,y,scale){
    v.save();v.translate(x,y);v.scale(scale,scale);
    v.fillStyle='#ad784a';v.fillRect(-20,-31,40,31);
    v.fillStyle='#dfaf75';v.beginPath();
    v.moveTo(-20,-31);v.lineTo(-12,-42);v.lineTo(28,-42);v.lineTo(20,-31);v.fill();
    v.fillStyle='#81522f';v.beginPath();
    v.moveTo(20,0);v.lineTo(28,-11);v.lineTo(28,-42);v.lineTo(20,-31);v.fill();
    v.fillStyle='#edd0a2';v.fillRect(-4,-31,8,26);
    v.restore();
}
function showScore(checkpoints, finished){
    const label=finished?'Final course score':'Course score';
    document.querySelector('#score').textContent=
        `${label}: ${checkpoints}/${data.result.total_checkpoints} checkpoint points`;
}
function showHint(checkpoints, finished, failure){
    const panel=document.querySelector('#hint');
    panel.hidden=!finished || data.result.reached_goal;
    if(panel.hidden)return;
    const hints={
        'Ran the stop sign':'Check what your code does when car.scan() returns "stop sign". Does it bring the car to a full stop before the line?',
        'Hit a pedestrian':'Check how your code reacts to "human". Does the car wait until the crossing is clear?',
        'Hit a box':'Check your distance reading just before contact. Did the car start steering around the box early enough?',
        'Crossed the course boundary':'Check the direction and duration of your last turn on the map.',
        'Stalled without making progress':'Scrub back a few steps. Is the car repeating the same turn or staying stopped after the way clears?'
    };
    const target=checkpoints<data.result.total_checkpoints
        ? `Checkpoint ${checkpoints+1} not reached.`
        : 'Finish area not reached.';
    const error=data.result.controller_errors[0];
    const hint=error ? `Start by investigating the controller error: ${error}`
        : hints[failure] ?? 'Trace the car on the map and compare its path with the next target.';
    const message=`${target} ${hint}`;
    if(panel.textContent!==message)panel.textContent=message;
}
function draw(position=i){if(!data.frames.length)return; i=Math.floor(position);x.clearRect(0,0,c.width,c.height);x.fillStyle='#d9f0df';x.fillRect(0,0,c.width,c.height);if(s.turningBulb){const [x,y,radius]=s.turningBulb;circle({x,y,radius},'#687079');}x.strokeStyle='#253746';x.lineWidth=8;for(const road of [s.route,...s.branches]){x.beginPath();road.forEach((p,n)=>n?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1]));x.stroke();if(s.turningBulb){x.strokeStyle='#687079';x.lineWidth=164;x.beginPath();road.filter(p=>p[0]>=835).forEach((p,n)=>n?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1]));x.stroke();}}s.obstacles.forEach(o=>circle(o,'#d9534f'));data.frames[i].objects.forEach(o=>circle(o,o.kind==='human'?'#7a4fa3':'#d22'));s.checkpoints.forEach((p,n)=>{circle(p,n<data.frames[i].checkpoint?'#8ccf72':'#f4c95d');x.fillStyle='#172b3a';x.fillText(n+1,p.x-3,p.y+4)});circle(s.goal,'#42b883');x.strokeStyle='#246b95';x.lineWidth=3;x.beginPath();data.frames.slice(0,i+1).forEach((f,n)=>n?x.lineTo(f.x,f.y):x.moveTo(f.x,f.y));x.stroke();const current=data.frames[i],next=data.frames[Math.min(i+1,data.frames.length-1)],fraction=position-i;const delta=((next.heading-current.heading+540)%360)-180;const f={...current,step:position,objects:current.objects.map((object,index)=>({...object,x:object.x+(next.objects[index].x-object.x)*fraction,y:object.y+(next.objects[index].y-object.y)*fraction})),x:current.x+(next.x-current.x)*fraction,y:current.y+(next.y-current.y)*fraction,heading:current.heading+delta*fraction};x.save();x.translate(f.x,f.y);x.rotate(f.heading*Math.PI/180);x.fillStyle='#247ba0';x.fillRect(-14,-9,28,18);x.fillStyle='white';x.fillRect(4,-5,8,10);x.restore();driverView(f);slider.value=i;document.querySelector('#step').textContent=`Step ${i+1}/${data.frames.length}`;showScore(current.checkpoint,i===data.frames.length-1);showHint(current.checkpoint,i===data.frames.length-1,current.failure);}
function pause(){if(t!==null)cancelAnimationFrame(t);t=null;}
function play(){
    if(t!==null){pause();return;}
    if(!data.frames.length)return;
    if(i===data.frames.length-1)i=0;
    let position=i;
    let previousTime;
    function animate(now){
        // Animation timestamps can precede the time recorded in the click handler.
        const elapsed=Math.min(50,Math.max(0,now-(previousTime??now)));
        previousTime=now;
        const crossing=data.frames[Math.floor(position)].objects.some(object=>object.walking);
        position=Math.min(data.frames.length-1,position+elapsed/(crossing?110:35));
        draw(position);
        t=position<data.frames.length-1?requestAnimationFrame(animate):null;
    }
    t=requestAnimationFrame(animate);
}
playButton.onclick=play;
document.querySelector('#reset').onclick=()=>{pause();i=0;draw()};
slider.oninput=e=>{pause();i=Number(e.target.value);draw()};
selector.onchange=selectCourse;
selectCourse();</script></body></html>"""
    output.write_text(template.replace("__DATA__", payload), encoding="utf-8")
