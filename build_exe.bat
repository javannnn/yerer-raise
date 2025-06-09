@echo off
REM Build standalone YererRaise.exe using PyInstaller
pyinstaller --onefile --noconsole -n YererRaise yererraise\app.py

