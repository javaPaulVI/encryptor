@echo off
REM Get the full path to this script's directory
set "SCRIPT_DIR=%~dp0"

REM Go up three levels to get to the 'encryption' folder
pushd "%SCRIPT_DIR%..\..\.."
set "ENCRYPTION_DIR=%cd%"
set "ZIPFILE=%ENCRYPTION_DIR%\encryption.zip"

REM Delete old zip if it already exists
if exist "%ZIPFILE%" del "%ZIPFILE%"

REM Use PowerShell to zip everything in the folder, excluding the .zip file
powershell -Command "Get-ChildItem -Path '%ENCRYPTION_DIR%' -Recurse -File | Where-Object { $_.FullName -ne '%ZIPFILE%' } | Compress-Archive -DestinationPath '%ZIPFILE%' -Force"

echo Created ZIP at: %ZIPFILE%
pause
popd
