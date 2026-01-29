@echo off
REM ==========================================
REM InterviewPilot Elite - Quick Start Script
REM ==========================================
REM This script starts both backend and frontend servers

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       InterviewPilot Elite - Quick Start                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Start Backend Server
echo [1/2] Starting Backend Server (Port 8080)...
echo.
start cmd /k "cd /d %~dp0 && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8080"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend Server  
echo.
echo [2/2] Starting Frontend Server (Port 3000)...
echo.
start cmd /k "cd /d %~dp0\frontend && python -m http.server 3000"

REM Wait for frontend to start
timeout /t 2 /nobreak

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              Servers Started Successfully!                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Backend:  http://localhost:8080
echo Frontend: http://localhost:3000
echo.
echo Open your browser and go to: http://localhost:3000
echo.
echo Credentials:
echo   Email:    test@example.com
echo   Password: password123
echo.
echo Windows will close these windows when you press Ctrl+C
echo Press any key to open the application in your default browser...
pause

REM Open in browser
start http://localhost:3000

echo.
echo Done! Application is running.
echo Keep these windows open while using the application.
echo.
