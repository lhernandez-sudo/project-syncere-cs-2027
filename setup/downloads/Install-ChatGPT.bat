@echo off
setlocal
title Project Syncere - Install ChatGPT

echo Project Syncere - ChatGPT Setup
echo.
echo This installs the official ChatGPT desktop app from the Microsoft Store.
echo Keep this window open until installation finishes.
echo.

where winget >nul 2>nul
if errorlevel 1 (
    echo ERROR: winget was not found.
    echo Install App Installer from the Microsoft Store or use https://chatgpt.com.
    echo Show this message to your instructor.
    echo.
    pause
    exit /b 1
)

winget install --id 9PLM9XGG6VKS --source msstore --accept-source-agreements --accept-package-agreements
set "INSTALL_EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%INSTALL_EXIT_CODE%"=="0" (
    echo ChatGPT did not install successfully.
    echo Use https://chatgpt.com and show this window to your instructor.
) else (
    echo ChatGPT installation finished.
    echo Open ChatGPT from the Windows Start menu and sign in.
)
echo.
pause
exit /b %INSTALL_EXIT_CODE%
