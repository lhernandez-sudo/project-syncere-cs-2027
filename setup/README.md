# Course Setup

## 1. Install the tools

Install the following software:

- Python 3.12 or newer
- Git
- Visual Studio Code
- The Python extension for Visual Studio Code

## 2. Clone the course repository

```bash
git clone https://github.com/lhernandez-sudo/project-syncere-cs-2027.git
cd project-syncere-cs-2027
```

## 3. Create a virtual environment

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS, Linux, or WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install course packages

```bash
python -m pip install -r requirements.txt
```

On systems where Python is named `python3`, use `python3` in place of `python`.

## 5. Verify the setup

```bash
python setup/verify_setup.py
```

You should see a success message and your installed Python version.

## Before each class

Open a terminal in the repository, activate the virtual environment, and run:

```bash
git pull
```
