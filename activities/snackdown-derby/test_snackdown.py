"""Launcher checks. Run with python -m unittest discover from this folder."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from snackdown_derby import build_page


class LauncherTests(unittest.TestCase):
    def test_supported_lengths_and_default(self):
        for duration in (180, 210, 240):
            page = build_page(duration)
            self.assertIn(f"const DURATION={duration}", page)
            self.assertNotIn("__DURATION__", page)
            self.assertIn("CHEESY", page)
            self.assertNotIn('<script src=', page)

    def test_rejects_out_of_scope_lengths(self):
        for duration in (0, 179, 241):
            with self.assertRaises(ValueError):
                build_page(duration)

    def test_single_file_launcher_exports_without_a_browser(self):
        with tempfile.TemporaryDirectory(prefix="snackdown-test-") as folder:
            output = Path(folder) / "show.html"
            result = subprocess.run([sys.executable, str(Path(__file__).with_name("snackdown_derby.py")),
                                     "--no-browser", "--output", str(output)],
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.exists())
            self.assertIn("SNACKDOWN", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
