@echo off
REM Quick Start Script - Smart City ML Platform

color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  Smart City ML Platform - Quick Start              ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Wait for pip to finish
timeout /t 5 /nobreak

echo [1] Training ML models...
python train_models.py

echo.
echo [2] Starting API server (keep this window open)...
echo.
echo API will be available at: http://localhost:8000/api/docs
echo.

venv\Scripts\python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

pause
