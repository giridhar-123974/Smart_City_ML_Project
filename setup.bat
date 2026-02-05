@echo off
REM Smart City ML Platform - Setup Script for Windows
REM This script automates the setup process on Windows

setlocal enabledelayedexpansion

cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   Smart City ML Platform - Windows Setup Script         ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check Python version
echo [1/6] Checking Python version...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python version: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo [4/6] Installing dependencies...
python -m pip install --upgrade pip setuptools wheel > nul 2>&1
pip install -r requirements.txt > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Train models
echo [5/6] Training ML models...
if not exist "models" (
    mkdir models
)
if not exist "models\air_quality_random_forest.pkl" (
    python train_models.py
    echo [OK] Models trained successfully
) else (
    echo [OK] Models already exist
)
echo.

REM Start services
echo [6/6] Setup complete!
echo.
echo ═══════════════════════════════════════════════════════
echo Setup completed successfully!
echo ═══════════════════════════════════════════════════════
echo.

echo Next steps:
echo.
echo Option 1: Run locally with separate terminals
echo   Terminal 1 - API Server:
echo     cd Smart_City_ML_Project
echo     python -m uvicorn backend.main:app --reload
echo.
echo   Terminal 2 - Dashboard:
echo     cd Smart_City_ML_Project
echo     streamlit run dashboard/app.py
echo.

echo Option 2: Run with Docker Compose
echo   docker-compose up --build
echo.

echo Access the application:
echo   API Docs: http://localhost:8000/api/docs
echo   Dashboard: http://localhost:8501
echo.

pause
