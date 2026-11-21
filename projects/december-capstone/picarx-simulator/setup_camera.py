"""Create an isolated camera environment and download the YOLO weights."""

from pathlib import Path
import os
import subprocess
import sys
import venv

HERE = Path(__file__).resolve().parent


def main() -> None:
    # PyTorch contains long filenames. Keep Windows paths short.
    environment = (
        Path.home() / ".venvs" / "picarx-camera"
        if os.name == "nt" else HERE / ".camera-venv"
    )
    # Include Raspberry Pi OS's system-installed Picamera2 and robot_hat.
    venv.EnvBuilder(with_pip=True, system_site_packages=True).create(environment)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run([str(python), "-m", "pip", "install", "-r",
                    str(HERE / "requirements-camera.txt")], check=True)
    subprocess.run(
        [str(python), "-c",
         "import sys; from ultralytics import YOLO; YOLO(sys.argv[1])",
         str(HERE / "yolo11n.pt")], check=True,
    )
    print(f"Camera environment ready. Python executable: {python}")
    print("Test an image first with camera_scanner.py --image photo.jpg.")


if __name__ == "__main__":
    main()
