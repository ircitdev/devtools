# ============================================
# UPDATE ALL DEVTOOLS PACKAGES
# ============================================

$DevTools = "D:\DevTools"
$ErrorActionPreference = "Continue"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   DEVTOOLS UPDATE UTILITY" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Python packages
Write-Host "[1/3] Updating Python packages..." -ForegroundColor Yellow
if (Test-Path "$DevTools\Python\venv\Scripts\python.exe") {
    try {
        Write-Host "  - Upgrading pip..." -ForegroundColor Gray
        & "$DevTools\Python\venv\Scripts\python.exe" -m pip install --upgrade pip --quiet

        Write-Host "  - Upgrading installed packages..." -ForegroundColor Gray
        $packages = & "$DevTools\Python\venv\Scripts\python.exe" -m pip list --outdated --format=json | ConvertFrom-Json

        if ($packages.Count -gt 0) {
            foreach ($pkg in $packages) {
                Write-Host "    Updating $($pkg.name)..." -ForegroundColor DarkGray
                & "$DevTools\Python\venv\Scripts\python.exe" -m pip install --upgrade $pkg.name --quiet
            }
            Write-Host "  ✓ Updated $($packages.Count) Python packages" -ForegroundColor Green
        } else {
            Write-Host "  ✓ All Python packages are up to date" -ForegroundColor Green
        }
    } catch {
        Write-Host "  ✗ Python update failed" -ForegroundColor Red
    }
} else {
    Write-Host "  ✗ Python venv not found" -ForegroundColor Red
}
Write-Host ""

# Node.js global packages
Write-Host "[2/3] Updating Node.js global packages..." -ForegroundColor Yellow
try {
    npm update -g 2>&1 | Out-Null
    Write-Host "  ✓ Node.js packages updated" -ForegroundColor Green
} catch {
    Write-Host "  ✗ npm update failed" -ForegroundColor Red
}
Write-Host ""

# Docker images
Write-Host "[3/3] Updating Docker images..." -ForegroundColor Yellow
try {
    $images = @("postgres:16-alpine", "redis:7-alpine", "mongo:7", "mysql:8")

    foreach ($image in $images) {
        Write-Host "  - Pulling $image..." -ForegroundColor Gray
        docker pull $image 2>&1 | Out-Null
    }
    Write-Host "  ✓ Docker images updated" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker update failed (is Docker running?)" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "============================================" -ForegroundColor Green
Write-Host "   UPDATE COMPLETE" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
