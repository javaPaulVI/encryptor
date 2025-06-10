@echo off
setlocal

REM Set Python installer URL (latest stable version for Windows 64-bit)
set "PYTHON_URL=https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"

REM Set installer filename
set "INSTALLER=python-installer.exe"

echo Downloading Python installer...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER%'"

if not exist "%INSTALLER%" (
    echo Failed to download Python installer.
    exit /b 1
)

echo Installing Python silently...
REM /quiet = silent, /passive = progress bar, /installallusers = install for all users
REM Prepend to PATH option is /prependpath
start /wait "" "%INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

if %ERRORLEVEL% neq 0 (
    echo Python installation failed with error %ERRORLEVEL%.
    exit /b %ERRORLEVEL%
)

echo Cleaning up installer file...
del "%INSTALLER%"

echo Python installed successfully!

REM Verify Python is on PATH
python --version
if %ERRORLEVEL% neq 0 (
    echo Python not found on PATH. You may need to restart your terminal or computer.
)

endlocal
pause
