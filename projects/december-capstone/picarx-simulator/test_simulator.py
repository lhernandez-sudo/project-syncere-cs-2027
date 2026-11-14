"""Instructor smoke tests for the simulator and compatibility API."""

import unittest

from simulator import Checkpoint, SceneObject, Scenario, VirtualPicarx, run_scenario, scenario_catalog
from student_controller import control_step


class SimulatorTests(unittest.TestCase):
    def test_api_clamps_unsafe_commands(self) -> None:
        car = VirtualPicarx(scenario_catalog()["practice"])
        car.forward(500)
        car.set_dir_servo_angle(-90)
        self.assertEqual(car.throttle, 100)
        self.assertEqual(car.steering, -35)
        self.assertEqual(car.invalid_commands, 2)

    def test_sensor_fault_is_repeatable(self) -> None:
        car = VirtualPicarx(scenario_catalog()["sensor_fault"])
        readings = [car.ultrasonic.read() for _ in range(9)]
        self.assertEqual(readings[-1], -1)

    def test_camera_returns_beginner_friendly_label(self) -> None:
        car = VirtualPicarx(scenario_catalog()["practice"])
        car.x, car.y, car.heading = 120, 290, 29
        self.assertEqual(car.scan(), "stop sign")

    def test_strict_starter_runs_stop_sign(self) -> None:
        result = run_scenario(control_step, scenario_catalog()["warehouse"], strict=True)
        self.assertFalse(result.reached_goal)
        self.assertEqual(result.stop_sign_violations, 1)
        self.assertEqual(result.replay[-1]["failure"], "Ran the stop sign")

    def test_running_roadside_stop_sign_ends_attempt(self) -> None:
        scenario = Scenario(
            "stop_test", 240, 120, (20, 60, 0), Checkpoint(215, 60, 20), (),
            route=((20, 60), (215, 60)),
            scene_objects=(SceneObject("stop sign", 105, 25),),
        )
        result = run_scenario(lambda car, memory: car.forward(35), scenario)
        self.assertEqual(result.stop_sign_violations, 1)
        self.assertFalse(result.reached_goal)
        self.assertTrue(result.stopped_safely)
        self.assertAlmostEqual(result.replay[-1]["x"], 105, delta=4)

    def test_pedestrian_collision_ends_attempt_before_goal(self) -> None:
        scenario = Scenario(
            "crossing_test", 240, 120, (20, 60, 0), Checkpoint(215, 60, 20), (),
            route=((20, 60), (215, 60)),
            scene_objects=(SceneObject("human", 105, 98, 12, (105, 22)),),
        )
        result = run_scenario(lambda car, memory: car.forward(55), scenario)
        self.assertEqual(result.human_hits, 1)
        self.assertFalse(result.reached_goal)
        self.assertLess(result.steps, scenario.max_steps)
        self.assertEqual(result.replay[-1]["failure"], "Hit a pedestrian")
        self.assertEqual(result.replay[-1]["throttle"], 0)

    def test_readable_turn_helpers_use_real_controls(self) -> None:
        car = VirtualPicarx(scenario_catalog()["practice"])
        car.turn_left(25)
        self.assertLess(car.steering, 0)
        self.assertEqual(car.throttle, 25)

    def test_stop_sign_controller_stops_then_resumes(self) -> None:
        scenario = Scenario(
            "stop_test", 240, 120, (20, 60, 0), Checkpoint(215, 60, 20), (), (),
            ((20, 60), (215, 60)), (SceneObject("stop sign", 105, 25),), max_steps=220,
        )

        def sign_controller(car, memory):
            seen = car.scan()
            if seen == "stop sign" and memory.get("wait", 0) < 12:
                memory["wait"] = memory.get("wait", 0) + 1
                car.stop()
            else:
                car.forward(35)

        result = run_scenario(sign_controller, scenario)
        self.assertTrue(result.reached_goal)
        self.assertEqual(result.stop_sign_violations, 0)
        self.assertEqual(result.stop_signs_obeyed, 1)

    def test_controller_errors_become_feedback(self) -> None:
        def broken_controller(car, memory):
            raise ValueError("student bug")

        result = run_scenario(broken_controller, scenario_catalog()["practice"])
        self.assertTrue(result.controller_errors)
        self.assertTrue(result.stopped_safely)

    def test_stationary_controller_does_not_reach_goal(self) -> None:
        def stopped_controller(car, memory):
            car.stop()

        result = run_scenario(stopped_controller, scenario_catalog()["practice"])
        self.assertFalse(result.reached_goal)
        self.assertEqual(result.distance_traveled, 0)


if __name__ == "__main__":
    unittest.main()
