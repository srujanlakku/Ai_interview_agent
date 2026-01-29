@echo off
REM Start InterviewPilot Backend and Frontend Servers
REM This script starts both servers in separate processes

setlocal enabledelayedexpansion

echo ============================================================
echo InterviewPilot - Server Startup Script
echo ============================================================
echo.

REM Set Python path
set PYTHONPATH=g:\projects\Interview-agent\backend

REM Kill any existing Python processes
taskkill /F /IM python.exe >nul 2>&1

echo Waiting for cleanup...
timeout /t 2 /nobreak >nul

REM Start Backend Server
echo Starting Backend Server on port 8080...
cd /d "g:\projects\Interview-agent\backend"
start "InterviewPilot Backend" python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

REM Start Frontend Server
echo Starting Frontend Server on port 3000...
cd /d "g:\projects\Interview-agent\frontend"
start "InterviewPilot Frontend" python -m http.server 3000

echo.
echo ============================================================
echo ✓ Servers started!
echo ============================================================
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8080
echo API Docs:  http://localhost:8080/docs
echo ============================================================
echo.
echo Close this window when done.
pause
