"""Run and score your PiCar-X controller, then play the replay."""

import argparse
import webbrowser
from pathlib import Path

from evaluate import write_score_report
from run_simulation import load_controller
from simulator import render_replays, run_scenario, scenario_catalog

HERE = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-browser", action="store_true",
                        help="Save the replay without opening it.")
    args = parser.parse_args()

    controller_path = HERE / "student_controller.py"
    report_path = HERE / "score_report.txt"
    replay_path = HERE / "strict_replay.html"
    try:
        controller = load_controller(controller_path)
    except Exception as error:
        print(f"Could not start student_controller.py: {type(error).__name__}: {error}")
        print("Fix the controller and run this script again. No new score or replay was saved.")
        return 1

    scenario = scenario_catalog()["warehouse"]
    result = run_scenario(controller, scenario, strict=True)
    score = write_score_report([result], controller_path, report_path)
    render_replays([(result, scenario)], replay_path, autoplay=True, evaluation_score=score)

    print(f"Score report: {report_path}")
    print(f"Replay: {replay_path}")
    if not args.no_browser and not webbrowser.open(replay_path.as_uri()):
        print("Open strict_replay.html in your browser to watch the run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
