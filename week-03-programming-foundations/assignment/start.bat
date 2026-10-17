@echo off
setlocal
title Project Syncere - Week 3 Output Tracker
cd /d "%~dp0"

set "COURSE_PYTHON=%~dp0..\..\.venv\Scripts\python.exe"

if exist "%COURSE_PYTHON%" (
    "%COURSE_PYTHON%" "%~dp0output_tracker.py"
) else (
    py -3 "%~dp0output_tracker.py"
)

echo.
echo Press any key to close the program.
pause >nul
