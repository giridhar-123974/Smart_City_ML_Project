@echo off
REM Start Dashboard Script - Smart City ML Platform

color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  Smart City ML Dashboard                           ║
echo ╚════════════════════════════════════════════════════╝
echo.

echo Starting Streamlit Dashboard...
echo Dashboard will open at: http://localhost:8501
echo.

cd Smart_City_ML_Project
streamlit run dashboard/app.py

pause
