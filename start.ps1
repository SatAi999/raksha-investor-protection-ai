# RAKSHA One-Command Startup Script (PowerShell)
Write-Host "=== STARTING RAKSHA SAFETY INFRASTRUCTURE ===" -ForegroundColor Cyan

# 1. Run Data & Model Verification
Write-Host "[1/3] Verifying models and database status..." -ForegroundColor Yellow
& D:\Computer_Vision\venv\Scripts\python.exe -m evaluation.run_all

# 2. Build Frontend static assets if needed
if (-not (Test-Path "frontend/dist/index.html")) {
    Write-Host "[2/3] Building frontend static assets..." -ForegroundColor Yellow
    Set-Location frontend
    npm run build
    Set-Location ..
}

# 3. Launch FastAPI Server on http://127.0.0.1:8000
Write-Host "[3/3] Launching FastAPI Backend & Production Web UI on http://127.0.0.1:8000 ..." -ForegroundColor Green
& D:\Computer_Vision\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
