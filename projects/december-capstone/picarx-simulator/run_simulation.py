"""Run one visible Virtual PiCar-X practice scenario."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from simulator import render_replays, run_scenario, scenario_catalog


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


def main(*, strict: bool = False) -> None:
    parser = argparse.ArgumentParser(description="Run the Virtual PiCar-X simulator")
    parser.add_argument("--controller", type=Path, default=HERE / "student_controller.py")
    default_replay = "strict_replay.html" if strict else "simulation_replay.html"
    parser.add_argument("--output", type=Path, default=HERE / default_replay)
    args = parser.parse_args()

    scenarios = scenario_catalog()
    scenario = scenarios["warehouse"]
    runs = [(run_scenario(load_controller(args.controller), scenario, strict=strict), scenario)]
    render_replays(runs, args.output)
    result, _ = runs[0]

    print(f"Scenario: {result.scenario}")
    print(f"Goal reached: {result.reached_goal}")
    print(f"Checkpoints: {result.checkpoints_reached}/{result.total_checkpoints}")
    print(f"Collisions: {result.collisions}; boundary hits: {result.boundary_hits}")
    print(f"Replay: {args.output}")
    if result.replay and result.replay[-1]["failure"]:
        print(f"Attempt ended: {result.replay[-1]['failure']}")
    if result.controller_errors:
        print("Controller error:", result.controller_errors[0])


if __name__ == "__main__":
    main()
