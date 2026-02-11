@echo off
setlocal enabledelayedexpansion

REM Guitar Tuner Web - Windows Launcher
REM This script activates the virtual environment and runs the Streamlit app

REM Set to the directory where this script is located
cd /d "%~dp0"

echo.
echo ========================================
echo   [*] Guitar Tuner Web - Launcher
echo ========================================
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo [!] ERROR: Virtual environment not found
    echo.
    echo Please run setup.ps1 first:
    echo   1. Right-click in Windows Explorer and select "Open PowerShell here"
    echo   2. Run: .\setup.ps1
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [!] ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [+] Virtual environment activated
echo.

REM Check if streamlit is installed
echo [*] Checking dependencies...
.venv\Scripts\python.exe -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [!] ERROR: Streamlit not installed
    echo.
    echo Please run setup.ps1 first
    echo.
    pause
    exit /b 1
)

echo [+] Dependencies verified
echo.
echo [*] Launching Guitar Tuner Web...
echo     App URL: http://localhost:8501
echo.
echo [*] Starting server in 2 seconds...
timeout /t 2 /nobreak
echo.

REM Open browser to the app
echo [*] Opening browser...
start http://localhost:8501
echo [+] Browser window should open shortly
echo.
echo [*] Press Ctrl+C in this window to stop the server
echo.

REM Launch streamlit 
.venv\Scripts\python.exe -m streamlit run app.py --logger.level=warning

REM If we get here, app has exited
echo.
echo [+] Application closed
echo.
pause
exit /b 0
