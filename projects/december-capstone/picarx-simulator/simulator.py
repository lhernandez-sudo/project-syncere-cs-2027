"""Deterministic, standard-library-only PiCar-X navigation simulator."""

from __future__ import annotations

from dataclasses import dataclass, field
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
class Scenario:
    name: str
    width: int
    height: int
    start: tuple[float, float, float]
    goal: Checkpoint
    obstacles: tuple[Circle, ...]
    checkpoints: tuple[Checkpoint, ...] = ()
    route: tuple[tuple[float, float], ...] = ()
    max_steps: int = 650
    sensor_fault_every: int = 0
    seed: int = 1


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
                for start, end in zip(self.scenario.route, self.scenario.route[1:])
            )
            readings.append(250 if route_distance <= 11 else 1200)
        return readings

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
        "practice", 900, 520, (65, 260, 0), Checkpoint(835, 260, 42),
        (Circle(350, 235, 38), Circle(610, 290, 38)),
        (Checkpoint(230, 350), Checkpoint(490, 350), Checkpoint(720, 225)),
        ((65, 260), (230, 350), (490, 350), (720, 225), (835, 260)), max_steps=700,
    )
    slalom = Scenario(
        "slalom", 900, 520, (65, 260, 0), Checkpoint(835, 260, 42),
        (Circle(260, 250, 38), Circle(445, 280, 38), Circle(620, 250, 38), Circle(735, 310, 34)),
        (Checkpoint(300, 375), Checkpoint(500, 130), Checkpoint(680, 385)),
        ((65, 260), (300, 375), (500, 130), (680, 385), (835, 260)), max_steps=850,
    )
    tight_turn = Scenario(
        "tight_turn", 760, 620, (70, 520, 270), Checkpoint(680, 90, 42),
        (Circle(190, 390, 48), Circle(380, 300, 52), Circle(570, 210, 48)),
        (Checkpoint(100, 260), Checkpoint(310, 100), Checkpoint(520, 430)),
        ((70, 520), (100, 260), (310, 100), (520, 430), (680, 90)), max_steps=900,
    )
    sensor_fault = Scenario(
        "sensor_fault", 900, 520, (65, 260, 0), Checkpoint(835, 260, 42),
        (Circle(350, 250, 38), Circle(600, 315, 38)),
        (Checkpoint(250, 150), Checkpoint(520, 150), Checkpoint(730, 250)),
        ((65, 260), (250, 150), (520, 150), (730, 250), (835, 260)),
        max_steps=800, sensor_fault_every=9,
    )
    rng = random.Random(271828)
    unseen_obstacles = tuple(Circle(rng.randint(230, 700), rng.randint(120, 400), rng.randint(34, 55)) for _ in range(4))
    unseen = Scenario(
        "unseen", 900, 520, (65, 260, 0), Checkpoint(835, 260, 42), unseen_obstacles,
        (Checkpoint(300, 95), Checkpoint(500, 430), Checkpoint(710, 95)),
        ((65, 260), (300, 95), (500, 430), (710, 95), (835, 260)), max_steps=900, seed=271828,
    )
    return {item.name: item for item in (practice, slalom, tight_turn, sensor_fault, unseen)}


def run_scenario(controller: Callable, scenario: Scenario) -> RunResult:
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

    for step_number in range(scenario.max_steps):
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

        if checkpoint_index < len(scenario.checkpoints):
            point = scenario.checkpoints[checkpoint_index]
            if distance((car.x, car.y), (point.x, point.y)) <= point.radius:
                checkpoint_index += 1

        if checkpoint_index == len(scenario.checkpoints) and distance((car.x, car.y), (scenario.goal.x, scenario.goal.y)) <= scenario.goal.radius:
            reached_goal = True
            car.stop()

        replay.append({
            "step": step_number, "x": round(car.x, 2), "y": round(car.y, 2),
            "heading": round(car.heading, 2), "steering": round(car.steering, 2),
            "throttle": round(car.throttle, 2), "checkpoint": checkpoint_index,
        })
        if reached_goal:
            break

    return RunResult(
        scenario.name, reached_goal, checkpoint_index, len(scenario.checkpoints), collisions,
        boundary_hits, car.invalid_commands, car.sensor_faults_seen, len(replay),
        round(distance_traveled, 2), steering_changes, abs(car.throttle) < 0.01,
        errors, replay,
    )


def render_replay(result: RunResult, scenario: Scenario, output: Path) -> None:
    payload = json.dumps({
        "result": {key: value for key, value in result.__dict__.items() if key != "replay"},
        "frames": result.replay,
        "scenario": {
            "name": scenario.name, "width": scenario.width, "height": scenario.height,
            "goal": scenario.goal.__dict__,
            "obstacles": [item.__dict__ for item in scenario.obstacles],
            "checkpoints": [item.__dict__ for item in scenario.checkpoints],
            "route": scenario.route,
        },
    })
    template = """<!doctype html><html><head><meta charset="utf-8"><title>Virtual PiCar-X Replay</title>
<style>body{font-family:Arial;background:#071b2e;color:white;margin:0;padding:22px}main{max-width:1050px;margin:auto}.card{background:#102d46;border:1px solid #2d6383;border-radius:14px;padding:16px;margin:12px 0}canvas{width:100%;background:#d9f0df;border-radius:10px}button,input{font-size:16px;margin-right:10px}strong{color:#55d6be}.legend span{margin-right:18px}</style></head>
<body><main><h1>Virtual PiCar-X Replay</h1><div class="card" id="summary"></div><canvas id="course"></canvas>
<div class="card"><button id="play">Play</button><button id="reset">Reset</button><input id="slider" type="range" min="0" value="0"><span id="step"></span></div>
<div class="legend"><span>🟦 Car</span><span>🟥 Obstacle</span><span>🟨 Checkpoint</span><span>🟩 Goal</span></div></main>
<script>const data=__DATA__,c=document.querySelector('#course'),x=c.getContext('2d'),s=data.scenario;c.width=s.width;c.height=s.height;
const slider=document.querySelector('#slider');slider.max=Math.max(0,data.frames.length-1);let i=0,t=null;
document.querySelector('#summary').innerHTML=`<strong>${s.name}</strong> — goal: ${data.result.reached_goal?'reached':'not reached'} | checkpoints: ${data.result.checkpoints_reached}/${data.result.total_checkpoints} | collisions: ${data.result.collisions} | boundary hits: ${data.result.boundary_hits}`;
function circle(o,color){x.beginPath();x.arc(o.x,o.y,o.radius,0,Math.PI*2);x.fillStyle=color;x.fill();}
function draw(){x.clearRect(0,0,c.width,c.height);x.fillStyle='#d9f0df';x.fillRect(0,0,c.width,c.height);x.strokeStyle='#253746';x.lineWidth=8;x.beginPath();s.route.forEach((p,n)=>n?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1]));x.stroke();s.obstacles.forEach(o=>circle(o,'#d9534f'));s.checkpoints.forEach((p,n)=>{circle(p,n<data.frames[i].checkpoint?'#8ccf72':'#f4c95d');x.fillStyle='#172b3a';x.fillText(n+1,p.x-3,p.y+4)});circle(s.goal,'#42b883');x.strokeStyle='#246b95';x.lineWidth=3;x.beginPath();data.frames.slice(0,i+1).forEach((f,n)=>n?x.lineTo(f.x,f.y):x.moveTo(f.x,f.y));x.stroke();const f=data.frames[i];x.save();x.translate(f.x,f.y);x.rotate(f.heading*Math.PI/180);x.fillStyle='#247ba0';x.fillRect(-14,-9,28,18);x.fillStyle='white';x.fillRect(4,-5,8,10);x.restore();slider.value=i;document.querySelector('#step').textContent=`Step ${i+1}/${data.frames.length}`}
function play(){if(t){clearInterval(t);t=null;return}t=setInterval(()=>{i++;if(i>=data.frames.length){i=data.frames.length-1;clearInterval(t);t=null}draw()},25)}
document.querySelector('#play').onclick=play;document.querySelector('#reset').onclick=()=>{i=0;draw()};slider.oninput=e=>{i=Number(e.target.value);draw()};draw();</script></body></html>"""
    output.write_text(template.replace("__DATA__", payload), encoding="utf-8")
