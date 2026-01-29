# InterviewPilot - Comprehensive Startup Script for Windows PowerShell
# Starts backend, frontend, and initializes database

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "InterviewPilot - Comprehensive Startup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Set Python path
$env:PYTHONPATH = "$PSScriptRoot\backend"

Write-Host "[1/4] Setting up environment..." -ForegroundColor Yellow
Write-Host "✓ Environment variables set" -ForegroundColor Green

Write-Host ""
Write-Host "[2/4] Initializing database..." -ForegroundColor Yellow
Push-Location "$PSScriptRoot\backend"
python -c "from app.models.database import Base, engine; Base.metadata.create_all(bind=engine); print('✓ Database tables created')"
python "$PSScriptRoot\backend\app\scripts\init_interview_db.py"
Pop-Location

Write-Host ""
Write-Host "[3/4] Starting backend server..." -ForegroundColor Yellow
$backendProcess = Start-Process -FilePath "python" `
    -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8080" `
    -WorkingDirectory "$PSScriptRoot\backend" `
    -PassThru `
    -WindowStyle Normal
Write-Host "✓ Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "[4/4] Starting frontend server..." -ForegroundColor Yellow
$frontendProcess = Start-Process -FilePath "python" `
    -ArgumentList "-m", "http.server", "3000" `
    -WorkingDirectory "$PSScriptRoot\frontend" `
    -PassThru `
    -WindowStyle Normal
Write-Host "✓ Frontend started (PID: $($frontendProcess.Id))" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "✓ InterviewPilot is ready!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Yellow
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Backend:   http://localhost:8080" -ForegroundColor Cyan
Write-Host "  API Docs:  http://localhost:8080/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Credentials for testing:" -ForegroundColor Yellow
Write-Host "  Email:    test@example.com" -ForegroundColor Magenta
Write-Host "  Password: password123" -ForegroundColor Magenta
Write-Host ""
Write-Host "25+ Indian MNCs available for interview preparation:" -ForegroundColor Yellow
Write-Host "  Big Tech (10): Google, Amazon, Microsoft, Meta, Apple..." -ForegroundColor Green
Write-Host "  Indian IT (5): TCS, Infosys, Wipro, HCL, Tech Mahindra" -ForegroundColor Green
Write-Host "  Startups (5): Flipkart, Swiggy, Zomato, Razorpay, Paytm" -ForegroundColor Green
Write-Host ""
Write-Host "11 Job Roles:" -ForegroundColor Yellow
Write-Host "  SDE, Backend, Frontend, Full Stack, Data Engineer, Data Scientist," -ForegroundColor Green
Write-Host "  AI/ML Engineer, DevOps, QA, System Design, Product Manager" -ForegroundColor Green
Write-Host ""
Write-Host "Close the terminal windows or press Ctrl+C to stop services" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Keep the script running
Write-Host "Press any key to stop the servers and close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Stop the processes
Write-Host ""
Write-Host "Stopping services..." -ForegroundColor Yellow
Stop-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue
Stop-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue
Write-Host "✓ All services stopped" -ForegroundColor Green
