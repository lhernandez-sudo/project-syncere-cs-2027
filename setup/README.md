# Day 1 Windows Setup

Students begin by downloading [`project-syncere-windows-setup.zip`](downloads/project-syncere-windows-setup.zip). They do not need Git or Python before running it.

The package contains:

- `Start-Setup.bat` - the file students double-click
- `install-windows.ps1` - the PowerShell installer used by the launcher
- `README.txt` - short student instructions

The setup installs:

- Python 3.12
- Git
- Visual Studio Code
- The Python extension for Visual Studio Code
- The Python packages required by this course

It then clones the course into the student's Documents folder, creates `.venv`, installs the course packages, verifies Python, and opens the course in Visual Studio Code. It is safe to run more than once.

## Student instructions

1. Connect the computer to the internet.
2. Open the [setup download](downloads/project-syncere-windows-setup.zip) on GitHub and select **Download raw file**.
3. Right-click the ZIP and select **Extract All**.
4. Open the extracted folder and double-click `Start-Setup.bat`.
5. Approve any Windows installation prompts.
6. Keep the setup window open until it reports success or an error.

Do not run the launcher from inside the ZIP preview. Extract all files first.

## Instructor preparation

Before Day 1:

1. Test the package on the same type of school-managed computer students will use.
2. Confirm that policy allows `winget`, PowerShell, GitHub, Python, Git, and Visual Studio Code.
3. Keep the ZIP in `setup/downloads/` synchronized with the source setup files.
4. Optionally publish the same ZIP as a GitHub Release asset for a larger download button.
5. Keep backup copies on the school LMS and a USB drive.
6. Provide students with a short link or QR code to the download.

If installation is blocked, ask school IT to preinstall the required software. The setup can then be rerun and will reuse installed packages.

## Confirm the setup manually

From the repository root:

```powershell
.\.venv\Scripts\python.exe setup\verify_setup.py
git --version
code --version
```

You should see a successful Python message plus installed Git and VS Code versions.

## If `winget` is missing

Install **App Installer** from the Microsoft Store, restart PowerShell, and run the script again. Ask the instructor for help before installing tools from another source.

## Before each class

Open PowerShell in the repository and run:

```powershell
git pull
.\.venv\Scripts\Activate.ps1
```

If script activation is blocked, use the environment's Python directly:

```powershell
git pull
.\.venv\Scripts\python.exe your_program.py
```
