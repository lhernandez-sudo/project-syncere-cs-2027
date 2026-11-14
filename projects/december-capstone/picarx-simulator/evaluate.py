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
    entry = next((node for node in tree.body
                  if isinstance(node, ast.FunctionDef) and node.name == "control_step"), None)
    helper_names = {node.name for node in functions} - {"control_step"}
    if entry and any(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        and node.func.id in helper_names for node in ast.walk(entry)
    ):
        points += 2
    else:
        notes.append("Move a distinct driving decision into a helper function and call it from control_step.")
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
    human_hits = sum(result.human_hits for result in results)
    stop_violations = sum(result.stop_sign_violations for result in results)
    invalid = sum(result.invalid_commands for result in results)
    errors = sum(bool(result.controller_errors) for result in results)
    safely_stopped = sum(
        result.stopped_safely and not (result.human_hits or result.stop_sign_violations)
        for result in results
    ) / count

    mission = 25 * goal_rate + 25 * checkpoint_rate
    safety = max(0, 15 * checkpoint_rate - crashes * 2.5 - human_hits * 8
                 - stop_violations * 5 - invalid * 0.5 - errors * 5)
    robustness = 10 * checkpoint_rate * safely_stopped * (1 - errors / count)
    efficient_runs = sum(
        result.reached_goal and result.steps < 650 and result.steering_changes < 120
        for result in results
    )
    efficiency = 5 * efficient_runs / count
    total = round(mission + safety + robustness + efficiency + quality_points, 1)

    feedback: list[str] = []
    if goal_rate < 0.6:
        feedback.append("Mission: tune navigation so the controller reaches more goals.")
    if crashes:
        feedback.append("Safety: slow down sooner or improve escape steering near obstacles and walls.")
    if human_hits:
        feedback.append("Human safety: stop earlier and wait before navigating around a person.")
    if stop_violations:
        feedback.append("Traffic rules: remain stopped long enough before passing a stop sign.")
    if goal_rate and efficiency < 5:
        feedback.append("Efficiency: reduce unnecessary steering changes or long recovery loops.")
    return min(90.0, total), feedback


def main() -> None:
    controller = load_controller(CONTROLLER)
    scenarios = scenario_catalog()
    results = [run_scenario(controller, scenarios["warehouse"], strict=True)]
    quality, quality_notes = code_quality(CONTROLLER)
    score, feedback = score_runs(results, quality)

    lines = [
        "VIRTUAL PICAR-X EVALUATION",
        "=" * 32,
        f"Automated score: {score}/90",
        f"Driving behavior: {round(score - quality, 1)}/80",
        f"Code quality: {quality}/10",
        "Instructor demonstration: ___/10",
        f"Possible final score: {score}/100 before demonstration points",
        "",
        "SCENARIOS",
    ]
    for result in results:
        lines.append(
            f"- {result.scenario:12} goal={str(result.reached_goal):5} "
            f"checkpoints={result.checkpoints_reached}/{result.total_checkpoints} "
            f"collisions={result.collisions} human_hits={result.human_hits} "
            f"stop_violations={result.stop_sign_violations} steps={result.steps}"
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
