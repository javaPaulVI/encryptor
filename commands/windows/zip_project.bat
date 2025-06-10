@echo off
REM Get the path to the folder containing this script
set "SCRIPT_DIR=%~dp0"

REM Go up three levels to get to the encryption folder
pushd "%SCRIPT_DIR%..\..\.."
set "ENCRYPTION_DIR=%cd%"
set "ZIPFILE=%ENCRYPTION_DIR%\encryption.zip"

REM Delete old zip if it exists (prevent recursive zipping)
if exist "%ZIPFILE%" del "%ZIPFILE%"

REM Zip the contents of the encryption folder (but not the zip file itself)
powershell -Command ^
    "$exclude = '%ZIPFILE%';" ^
    "Add-Type -AssemblyName 'System.IO.Compression.FileSystem';" ^
    "$zip = [System.IO.Compression.ZipFile]::Open('$ZIPFILE', 'Create');" ^
    "Get-ChildItem -Path '.' -Recurse | Where-Object { -not $_.PSIsContainer -and $_.FullName -ne $exclude } | ForEach-Object {" ^
    "  $entryName = $_.FullName.Substring($env:ENCRYPTION_DIR.Length + 1);" ^
    "  [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $entryName);" ^
    "}; $zip.Dispose()"

echo Created ZIP inside: %ZIPFILE%
pause
popd
