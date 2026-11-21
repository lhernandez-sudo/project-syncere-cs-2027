"""Verify bundled notebooks replace stale runtime modules without restarting."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class NotebookRuntimeTests(unittest.TestCase):
    def test_student_notebook_recovers_from_old_imports(self):
        notebook = Path(__file__).with_name("picarx-camera-decisions.ipynb")
        script = r'''
import json, sys, types
from dataclasses import dataclass

old_simulator = types.ModuleType("simulator")
@dataclass
class OldScenario:
    name: str
old_simulator.Scenario = OldScenario
sys.modules["simulator"] = old_simulator
old_course = types.ModuleType("guided_course")
old_course.run_guided_course = lambda *args: (_ for _ in ()).throw(RuntimeError("stale course"))
sys.modules["guided_course"] = old_course

nb = json.load(open(sys.argv[1], encoding="utf-8"))
setup = next("".join(c["source"]) for c in nb["cells"] if c["cell_type"]=="code" and "bundled_sources = json.loads(" in "".join(c["source"]))
controller = "".join(nb["cells"][3]["source"])
namespace = {}
for repeat in range(2):
    exec(setup, namespace)
    exec(controller, namespace)
    # Verify that the distributed notebook still contains unfinished starters.
    assert namespace["is_stop_signal"]("human") is False
    assert namespace["launch_countdown"](5) == []
    assert namespace["launch_countdown"](0) == []
    assert "road_half_width" in sys.modules["simulator"].Scenario.__dataclass_fields__
    assert sys.modules["simulator"] is not old_simulator
    result, scenario = namespace["run_guided_course"](
        namespace["control_step"], namespace["custom_object"], namespace["avoid_direction"])
    assert not result.reached_goal and result.checkpoints_reached == 0
    assert "No progress" in result.replay[-1]["failure"]
    assert scenario.road_half_width == 85
    assert sys.path.count(str(namespace["work_folder"])) == 1
    from simulator import render_replays
    render_replays([(result, scenario)], namespace["work_folder"] / "verified.html")
print("Recovered stale imports, kept unfinished starters, rendered HTML, and reran setup successfully.")
'''
        for filename in (notebook.name,):
            with self.subTest(notebook=filename):
                with tempfile.TemporaryDirectory(prefix="picarx-runtime-") as folder:
                    result = subprocess.run([sys.executable, "-c", script, str(notebook.with_name(filename))],
                                            cwd=folder, capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Recovered stale imports", result.stdout)


if __name__ == "__main__":
    unittest.main()
