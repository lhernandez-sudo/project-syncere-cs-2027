"""Run one visible Virtual PiCar-X practice scenario."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from simulator import render_replay, run_scenario, scenario_catalog


HERE = Path(__file__).resolve().parent


def load_controller(path: Path):
    spec = importlib.util.spec_from_file_location("student_controller", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "control_step"):
        raise AttributeError("student_controller.py must define control_step(car, memory)")
    return module.control_step


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Virtual PiCar-X simulator")
    parser.add_argument("--scenario", default="practice", choices=sorted(scenario_catalog()))
    parser.add_argument("--controller", type=Path, default=HERE / "student_controller.py")
    parser.add_argument("--output", type=Path, default=HERE / "simulation_replay.html")
    args = parser.parse_args()

    scenario = scenario_catalog()[args.scenario]
    result = run_scenario(load_controller(args.controller), scenario)
    render_replay(result, scenario, args.output)

    print(f"Scenario: {result.scenario}")
    print(f"Goal reached: {result.reached_goal}")
    print(f"Checkpoints: {result.checkpoints_reached}/{result.total_checkpoints}")
    print(f"Collisions: {result.collisions}; boundary hits: {result.boundary_hits}")
    print(f"Replay: {args.output}")
    if result.controller_errors:
        print("Controller error:", result.controller_errors[0])


if __name__ == "__main__":
    main()
