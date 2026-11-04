@echo off
chcp 65001 >nul
title Todo App - Sprint 1 Launcher

echo =======================================================
echo   Todo App - Automatic Setup and Launcher
echo =======================================================

REM Check if virtual environment exists and is valid on this machine
".venv\Scripts\python.exe" -c "import fastapi, uvicorn, sqlalchemy" >nul 2>nul
if errorlevel 1 (
    echo [*] Setting up Python virtual environment and dependencies...
    python -m venv --clear .venv
    if errorlevel 1 (
        echo [!] Error: Python 3.10+ is not installed or not in PATH.
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install --upgrade pip >nul 2>nul
    ".venv\Scripts\pip.exe" install -r requirements.txt
    if errorlevel 1 (
        echo [!] Error installing dependencies from requirements.txt
        pause
        exit /b 1
    )
    echo [+] Environment setup complete!
)

echo [*] Starting Todo App server...
".venv\Scripts\python.exe" run.py
pause
