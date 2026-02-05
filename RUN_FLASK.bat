@echo off
REM Quick start script for Smart City ML Flask Application

echo.
echo 🚀 Starting Smart City ML Flask Application...
echo.

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Create directories
if not exist models mkdir models
if not exist logs mkdir logs
if not exist uploads mkdir uploads

REM Start Flask app
echo.
echo ✨ Starting Flask application...
echo 🌐 Open browser: http://localhost:5000
echo 📝 Default login - Create account on signup page
echo.

python app.py

pause
