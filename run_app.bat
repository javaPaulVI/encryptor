@echo off
setlocal

REM Get full path to venv activate script
set "VENV_ACTIVATE=%~dp0venv\Scripts\activate.bat"

REM Check if venv exists
if not exist "%VENV_ACTIVATE%" (
    python -m venv "%~dp0\venv"
    if errorlevel 1 (
        echo Failed to create virtual environment. Please ensure Python is installed.
        exit /b 1
    )
    echo Virtual environment created at %~dp0venv
)

REM Activate the venv
call "%VENV_ACTIVATE%"

REM Check and install Flask
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
)

REM Check and install cryptography
pip show cryptography >nul 2>&1
if errorlevel 1 (
    echo Installing cryptography...
    pip install cryptography
)

REM Open default browser
start "" "http://127.0.0.1:5000"

REM Launch Flask app in a new, detached cmd window
start "" cmd /k "cd /d %~dp0 && venv\Scripts\python app.py"

endlocal

