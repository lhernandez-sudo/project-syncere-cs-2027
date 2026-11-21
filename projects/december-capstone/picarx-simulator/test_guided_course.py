"""Continuous scene and beginner-controller integration checks."""
import contextlib
import io
import unittest
from dataclasses import fields, make_dataclass, MISSING
from unittest.mock import patch

from guided_course import run_guided_course


class TestCar:
    def __init__(self):
        self.label = "clear"
        self.distance = 200
        self.action = "stop"
        self.steering = 0
        self.history = []
        self.ultrasonic = self

    def scan(self):
        return self.label

    def read(self):
        return self.distance

    def stop(self):
        self.action = "stop"
        self.history.append(("stop", 0))

    def forward(self, speed):
        self.action = "forward"
        self.history.append(("forward", speed))

    def set_dir_servo_angle(self, angle):
        self.steering = angle


def driver(direction):
    def step(car, memory):
        label = car.scan()
        if label in ("human", "stop sign") or car.ultrasonic.read() < 25:
            car.stop()
        elif label == "pizza box":
            car.set_dir_servo_angle(-25 if direction == "left" else 25)
            car.forward(30)
        else:
            car.set_dir_servo_angle(0)
            car.forward(30)
    return step


class GuidedCourseTests(unittest.TestCase):
    def run_course(self, controller, direction="left"):
        with contextlib.redirect_stdout(io.StringIO()):
            return run_guided_course(controller, "pizza box", direction, TestCar)[0]

    def test_beginner_rules_finish_both_sides(self):
        for direction in ("left", "right"):
            with self.subTest(direction=direction):
                result = self.run_course(driver(direction), direction)
                self.assertTrue(result.reached_goal)
                self.assertEqual(result.checkpoints_reached, 5)
                self.assertEqual(result.stop_signs_obeyed, 1)
                self.assertEqual(result.collisions, 0)

    def test_objects_persist_and_move_continuously(self):
        frames = self.run_course(driver("left")).replay
        identities = {o["id"] for o in frames[0]["objects"]}
        for frame in frames:
            self.assertEqual({o["id"] for o in frame["objects"]}, identities)
        for identity in ("roadside-sign", "personal-object"):
            positions = {(o["x"],o["y"]) for f in frames for o in f["objects"] if o["id"] == identity}
            self.assertEqual(len(positions), 1)
        for before, after in zip(frames, frames[1:]):
            self.assertLess(abs(after["x"]-before["x"]), 4)
            self.assertLess(abs(after["y"]-before["y"]), 4)
            for old, new in zip(before["objects"], after["objects"]):
                self.assertLess(abs(new["y"]-old["y"]), 3)
        pedestrian_before_wait = any(f["throttle"] > 0 and 165 < f["objects"][0]["y"] < 355 for f in frames)
        self.assertTrue(pedestrian_before_wait)
        self.assertEqual(frames[-1]["objects"][2]["y"], 390)

    def test_unsafe_and_stalled_controllers_fail(self):
        unsafe = self.run_course(lambda car, memory: car.forward(30))
        self.assertFalse(unsafe.reached_goal)
        self.assertIn("pedestrian", unsafe.replay[-1]["failure"])
        stalled = self.run_course(lambda car, memory: car.stop())
        self.assertFalse(stalled.reached_goal)
        self.assertIn("No progress", stalled.replay[-1]["failure"])

    def test_legacy_scenario_constructor_without_road_width(self):
        from simulator import Scenario
        definitions = []
        for field in fields(Scenario):
            if field.name == "road_half_width":
                continue
            if field.default is MISSING:
                definitions.append((field.name, field.type))
            else:
                definitions.append((field.name, field.type, field.default))
        LegacyScenario = make_dataclass("LegacyScenario", definitions, frozen=True)
        with patch("simulator.Scenario", LegacyScenario):
            result = self.run_course(driver("left"))
        self.assertTrue(result.reached_goal)
        self.assertEqual(result.checkpoints_reached, 5)


if __name__ == "__main__":
    unittest.main()
