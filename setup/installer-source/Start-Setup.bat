@echo off
setlocal
title Project Syncere Windows Setup

echo Project Syncere Windows Setup
echo.
echo This installs Python, Git, and Visual Studio Code.
echo It also downloads and configures the course repository.
echo Keep this window open until setup finishes.
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-windows.ps1"
set "SETUP_EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%SETUP_EXIT_CODE%"=="0" (
    echo Setup did not finish successfully.
    echo Show this window to your instructor before closing it.
) else (
    echo Setup finished successfully.
)
echo.
pause
exit /b %SETUP_EXIT_CODE%
