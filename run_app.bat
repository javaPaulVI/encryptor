@echo off
setup.bat

REM Open default browser
start "" "http://localhost:1449"

REM Launch Flask app in a new, detached cmd window
start "" cmd /k "cd /d %~dp0 && venv\Scripts\python app.py"

endlocal

