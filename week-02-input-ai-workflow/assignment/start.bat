@echo off
setlocal
title Project Syncere - Week 2 Adventure
cd /d "%~dp0"

set "COURSE_PYTHON=%~dp0..\..\.venv\Scripts\python.exe"

if exist "%COURSE_PYTHON%" (
    "%COURSE_PYTHON%" "%~dp0adventure.py"
) else (
    py -3 "%~dp0adventure.py"
)

echo.
echo Press any key to close the program.
pause >nul
