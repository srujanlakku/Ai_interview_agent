@echo off
REM InterviewPilot Quick Start Script for Windows

echo.
echo Launching InterviewPilot...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.9+
    exit /b 1
)
echo [OK] Python found

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 16+
    exit /b 1
)
echo [OK] Node.js found

echo.
echo Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

if not exist ".env" (
    copy .env.example .env
    echo [WARNING] .env file created. Please update with your API keys
)

echo Installing backend dependencies...
pip install -q -r requirements.txt

echo Starting backend server...
start cmd /k "python -m uvicorn app.main:app --reload"

cd ..

echo.
echo Setting up frontend...
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install -q
)

echo Starting frontend server...
start cmd /k "npm run dev"

cd ..

echo.
echo [SUCCESS] InterviewPilot services started!
echo.
echo Services:
echo - Backend API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo - Frontend: http://localhost:3000
echo.
echo Next steps:
echo 1. Update backend\.env with your API keys
echo 2. Open http://localhost:3000 in your browser
echo 3. Create an account and start preparing!
echo.
pause
