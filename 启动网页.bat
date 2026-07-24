@echo off
title mdtoolkit web demo

echo ============================================
echo   Starting mdtoolkit web demo, please wait...
echo ============================================
echo.

cd /d "%~dp0"

REM Check python exists
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python first: https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

REM Check flask; install if missing
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo First run: installing dependency "flask", please wait...
    python -m pip install flask
    echo.
    python -c "import flask" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to install flask. Please run manually:  pip install flask
        pause
        exit /b 1
    )
)

echo Starting server, browser will open automatically.
echo Close this window to stop the server.
echo.

python web_api.py

pause
