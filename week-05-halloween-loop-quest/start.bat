@echo off
cd /d "%~dp0"
py -3 examples\haunted_mushroom_kingdom.py
if errorlevel 1 python examples\haunted_mushroom_kingdom.py
pause
