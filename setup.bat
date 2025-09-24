@echo off
REM setup_venv.bat - Windows virtual environment setup script

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%.venv"

echo Setting up virtual environment for rlooper_sim_python...
echo Project directory: %PROJECT_DIR%

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
) else (
    echo Virtual environment already exists at %VENV_DIR%
)

REM Activate virtual environment and install requirements
echo Installing requirements...
call "%VENV_DIR%\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r "%PROJECT_DIR%requirements.txt"

echo.
echo ✅ Setup complete!
echo.
echo To activate the virtual environment:
echo   %VENV_DIR%\Scripts\activate.bat
echo   Or in PowerShell: %VENV_DIR%\Scripts\Activate.ps1
echo.
echo To run the workflow:
echo   python run_workflow.py all
echo.
pause