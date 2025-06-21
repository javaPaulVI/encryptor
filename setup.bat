@echo off
setlocal EnableDelayedExpansion

REM Get the current script directory with trailing backslash and normalized case (lowercase)
set "SCRIPT_DIR=%~dp0"

REM Remove trailing backslash from SCRIPT_DIR if any for consistent checking
if "!SCRIPT_DIR:~-1!"=="\" set "SCRIPT_DIR=!SCRIPT_DIR:~0,-1!"

REM Add SCRIPT_DIR to current session PATH if not already present
echo %PATH% | findstr /I /C:"!SCRIPT_DIR!" >nul
if errorlevel 1 (
    REM Not in current session PATH, add it now
    set "PATH=%PATH%;%SCRIPT_DIR%"
)

REM Fetch current user PATH from registry
for /f "tokens=2,*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul ^| findstr /i PATH') do set "USER_PATH=%%B"

REM Remove trailing backslash from USER_PATH entries for accurate match (optional)
REM Actually trimming all entries is complex in batch, so we'll do a simpler check:

REM Add semicolons at start and end to avoid partial matches
set "CHECK_PATH=;%USER_PATH%;"

REM Remove trailing backslash from SCRIPT_DIR again just in case
if "!SCRIPT_DIR:~-1!"=="\" set "SCRIPT_DIR=!SCRIPT_DIR:~0,-1!"

REM Check if SCRIPT_DIR already in USER_PATH (case insensitive)
echo !CHECK_PATH! | findstr /I /C:";!SCRIPT_DIR!;" >nul
if errorlevel 1 (
    REM Not in permanent user PATH, add it
    echo Adding %SCRIPT_DIR% to permanent PATH
    REM Append ; and script dir to USER_PATH (avoid double semicolon)
    if "!USER_PATH:~-1!"==";" (
        set "NEW_PATH=!USER_PATH!!SCRIPT_DIR!"
    ) else (
        set "NEW_PATH=!USER_PATH!;%SCRIPT_DIR%"
    )
    REM Update user PATH permanently
    endlocal
    setx PATH "%NEW_PATH%" >nul
) else (
    endlocal
    REM Already in permanent PATH, do nothing
)

REM Now reactivate delayed expansion for rest of script if needed
setlocal EnableDelayedExpansion

REM Check if the virtual environment activate script exists
set "VENV_ACTIVATE=%SCRIPT_DIR%\venv\Scripts\activate.bat"
if not exist "%VENV_ACTIVATE%" (
    echo Creating virtual environment...
    python -m venv "%SCRIPT_DIR%\venv"
    if errorlevel 1 (
        echo Failed to create virtual environment. Please ensure Python is installed and accessible.
        exit /b 1
    )
    echo Virtual environment created at %SCRIPT_DIR%\venv
)

REM Activate the virtual environment
call "%VENV_ACTIVATE%"

REM Check and install Flask if missing
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
)

REM Check and install cryptography if missing
pip show cryptography >nul 2>&1
if errorlevel 1 (
    echo Installing cryptography...
    pip install cryptography
)

REM No echo if everything is fine

endlocal
