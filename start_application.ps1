#!/usr/bin/env pwsh
# ==========================================
# InterviewPilot Elite - Quick Start Script
# ==========================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       InterviewPilot Elite - Quick Start                  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Backend Server
Write-Host "[1/2] Starting Backend Server (Port 8080)..." -ForegroundColor Green
Write-Host ""

$backendProcess = Start-Process -FilePath "python" `
    -ArgumentList "-m uvicorn backend.app.main:app --host 0.0.0.0 --port 8080" `
    -WorkingDirectory $scriptDir `
    -PassThru `
    -NoNewWindow

Write-Host "Backend process started (PID: $($backendProcess.Id))" -ForegroundColor Green
Start-Sleep -Seconds 3

# Start Frontend Server
Write-Host ""
Write-Host "[2/2] Starting Frontend Server (Port 3000)..." -ForegroundColor Green
Write-Host ""

$frontendDir = Join-Path $scriptDir "frontend"
$frontendProcess = Start-Process -FilePath "python" `
    -ArgumentList "-m http.server 3000" `
    -WorkingDirectory $frontendDir `
    -PassThru `
    -NoNewWindow

Write-Host "Frontend process started (PID: $($frontendProcess.Id))" -ForegroundColor Green
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              Servers Started Successfully!                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:8080" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Open your browser and go to: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Credentials:" -ForegroundColor Yellow
Write-Host "  Email:    test@example.com"
Write-Host "  Password: password123"
Write-Host ""
Write-Host "Press Ctrl+C to stop the servers" -ForegroundColor Red
Write-Host ""

# Open in browser
Start-Process "http://localhost:3000"

Write-Host "Servers are running. Press Ctrl+C to stop." -ForegroundColor Green
Write-Host ""

# Keep the script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Check if processes are still running
        if (-not (Get-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue)) {
            Write-Host "Backend process has stopped." -ForegroundColor Red
            break
        }
        
        if (-not (Get-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue)) {
            Write-Host "Frontend process has stopped." -ForegroundColor Red
            break
        }
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
} finally {
    # Clean up processes if script is stopped
    try {
        Stop-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue
        Stop-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue
    } catch {
        # Ignore errors during cleanup
    }
    
    Write-Host ""
    Write-Host "Servers have been stopped." -ForegroundColor Yellow
    Write-Host ""
}
