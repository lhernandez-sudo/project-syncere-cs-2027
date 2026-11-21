"""Perception policy and motor-stop regression checks without camera packages."""

import unittest
from unittest.mock import Mock

from camera_scanner import CameraScanner, Detection
from car_api import HardwarePicarx


class CameraTests(unittest.TestCase):
    def setUp(self):
        self.scanner = CameraScanner.__new__(CameraScanner)
        self.scanner.person_until = 0.0
        self.scanner.sign_until = 0.0
        self.scanner.person_hold = 0.8
        self.scanner.sign_hold = 0.4
        self.scanner.minimum_sign_area = 0.005

    def test_person_priority_and_dropout_hold(self):
        person = Detection("human", 0.9, (0.3, 0.1, 0.7, 0.9))
        sign = Detection("stop sign", 0.8, (0.8, 0.2, 0.95, 0.5))
        self.assertEqual(self.scanner.select_label([sign, person], 10), "human")
        self.assertEqual(self.scanner.select_label([], 10.5), "human")
        self.assertEqual(self.scanner.select_label([], 11), "clear")

    def test_tiny_sign_is_ignored_and_visible_sign_is_held(self):
        tiny = Detection("stop sign", 0.9, (0.1, 0.1, 0.11, 0.11))
        self.assertEqual(self.scanner.select_label([tiny], 10), "clear")
        sign = Detection("stop sign", 0.9, (0.1, 0.1, 0.3, 0.3))
        self.assertEqual(self.scanner.select_label([sign], 11), "stop sign")
        self.assertEqual(self.scanner.select_label([], 11.2), "stop sign")
        self.assertEqual(self.scanner.select_label([], 12), "clear")

    def test_capture_failure_stops_motor_before_raising(self):
        car = HardwarePicarx.__new__(HardwarePicarx)
        car.stop = Mock()
        car._scanner = Mock(side_effect=RuntimeError("No camera"))
        with self.assertRaisesRegex(RuntimeError, "No camera"):
            car.scan()
        car.stop.assert_called_once()

    def test_invalid_camera_label_stops(self):
        car = HardwarePicarx.__new__(HardwarePicarx)
        car.stop = Mock()
        car._scanner = lambda: "unknown"
        with self.assertRaises(ValueError):
            car.scan()
        self.assertTrue(car.stop.called)


if __name__ == "__main__":
    unittest.main()
