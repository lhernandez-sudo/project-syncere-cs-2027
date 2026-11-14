"""Instructor smoke tests for the simulator and compatibility API."""

import unittest

from simulator import VirtualPicarx, run_scenario, scenario_catalog


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
