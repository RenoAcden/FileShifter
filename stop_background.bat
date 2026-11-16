@echo off
echo Stopping background file organizer...
taskkill /f /im pythonw.exe 2>nul
if %errorlevel% equ 0 (
    echo File organizer stopped successfully.
) else (
    echo File organizer was not running.
)
pause
