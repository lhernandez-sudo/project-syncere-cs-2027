@echo off
cd /d "%~dp0"
py -3 output_tracker_rebuild.py
if errorlevel 1 python output_tracker_rebuild.py
pause
