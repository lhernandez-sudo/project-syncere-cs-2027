"""Transparent scoring harness for the Virtual PiCar-X capstone."""

from __future__ import annotations

import ast
from pathlib import Path

from run_simulation import load_controller
from simulator import RunResult, run_scenario, scenario_catalog


HERE = Path(__file__).resolve().parent
CONTROLLER = HERE / "student_controller.py"


def code_quality(path: Path) -> tuple[float, list[str]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    notes: list[str] = []
    points = 0.0
    if any(node.name == "control_step" for node in functions):
        points += 2
    if len(functions) >= 2:
        points += 2
    else:
        notes.append("Add at least one helper function.")
    if all((node.end_lineno or node.lineno) - node.lineno <= 35 for node in functions):
        points += 2
    else:
        notes.append("Break long functions into smaller jobs.")
    names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
    short_names = [name for name in names if len(name) == 1 and name not in {"x", "y"}]
    if len(short_names) <= 2:
        points += 2
    else:
        notes.append("Use descriptive variable names.")
    if "#" in source and any(ast.get_docstring(node) for node in functions):
        points += 2
    else:
        notes.append("Document the reason for important decisions.")
    return points, notes


def score_runs(results: list[RunResult], quality_points: float) -> tuple[float, list[str]]:
    count = len(results)
    goal_rate = sum(result.reached_goal for result in results) / count
    checkpoint_total = sum(result.total_checkpoints for result in results)
    checkpoint_rate = sum(result.checkpoints_reached for result in results) / max(1, checkpoint_total)
    crashes = sum(result.collisions + result.boundary_hits for result in results)
    invalid = sum(result.invalid_commands for result in results)
    errors = sum(bool(result.controller_errors) for result in results)
    safely_stopped = sum(result.stopped_safely for result in results) / count

    mission = 22 * goal_rate + 8 * checkpoint_rate
    safety = max(0, 25 - crashes * 2.5 - invalid * 0.5 - errors * 5)
    fault_result = next(item for item in results if item.scenario == "sensor_fault")
    unseen_result = next(item for item in results if item.scenario == "unseen")
    robustness = 5 * safely_stopped + 5 * (not fault_result.controller_errors) + 5 * (
        unseen_result.reached_goal or unseen_result.checkpoints_reached >= 2
    )
    efficient_runs = sum(result.steps < 650 and result.steering_changes < 120 for result in results)
    efficiency = 10 * efficient_runs / count
    total = round(mission + safety + robustness + efficiency + quality_points, 1)

    feedback: list[str] = []
    if goal_rate < 0.6:
        feedback.append("Mission: tune navigation so the controller reaches more goals.")
    if crashes:
        feedback.append("Safety: slow down sooner or improve escape steering near obstacles and walls.")
    if fault_result.controller_errors:
        feedback.append("Robustness: handle an ultrasonic value of -1 without crashing.")
    if not unseen_result.reached_goal:
        feedback.append("Generalization: avoid hard-coded moves tied to the practice map.")
    if efficiency < 7:
        feedback.append("Efficiency: reduce unnecessary steering changes or long recovery loops.")
    return min(90.0, total), feedback


def main() -> None:
    controller = load_controller(CONTROLLER)
    scenarios = scenario_catalog()
    results = [run_scenario(controller, scenario) for scenario in scenarios.values()]
    quality, quality_notes = code_quality(CONTROLLER)
    score, feedback = score_runs(results, quality)

    lines = [
        "VIRTUAL PICAR-X EVALUATION",
        "=" * 32,
        f"Automated score: {score}/90",
        "Instructor demonstration: ___/10",
        f"Possible final score: {score}/100 before demonstration points",
        "",
        "SCENARIOS",
    ]
    for result in results:
        lines.append(
            f"- {result.scenario:12} goal={str(result.reached_goal):5} "
            f"checkpoints={result.checkpoints_reached}/{result.total_checkpoints} "
            f"collisions={result.collisions} boundaries={result.boundary_hits} steps={result.steps}"
        )
    lines.extend(["", "NEXT IMPROVEMENTS"])
    for note in feedback + quality_notes:
        lines.append(f"- {note}")
    if not feedback and not quality_notes:
        lines.append("- Strong result. Explain why the design works and identify one remaining limitation.")
    report = "\n".join(lines) + "\n"
    (HERE / "score_report.txt").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
