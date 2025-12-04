# ============================================
# PORTABLE PYTHON SETUP FOR D:\DevTools
# ============================================

$ErrorActionPreference = "Stop"
$DevTools = "D:\DevTools"
$PythonDir = "$DevTools\Python"
$PythonPortable = "$PythonDir\portable"
$PythonVenv = "$PythonDir\venv"

Write-Host "Setting up Portable Python Environment..." -ForegroundColor Cyan

# Create directories
$dirs = @($PythonPortable, $PythonVenv)
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Check if Python is installed
$systemPython = "C:\Python311\python.exe"
if (-not (Test-Path $systemPython)) {
    Write-Host "ERROR: Python not found at $systemPython" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ first" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found Python: $systemPython" -ForegroundColor Green

# Create symbolic link or copy Python
$portablePython = "$PythonPortable\python.exe"
if (-not (Test-Path $portablePython)) {
    Write-Host "Creating portable Python reference..." -ForegroundColor Yellow
    Copy-Item -Path $systemPython -Destination $portablePython -Force
    Copy-Item -Path "C:\Python311\python311.dll" -Destination "$PythonPortable\" -Force -ErrorAction SilentlyContinue
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "$PythonVenv\Scripts\python.exe")) {
    & $systemPython -m venv $PythonVenv
    Write-Host "Virtual environment created!" -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Green
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& "$PythonVenv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel --quiet

# Install essential packages
Write-Host "Installing essential Python packages..." -ForegroundColor Yellow
$packages = @(
    "requests",
    "aiohttp",
    "fastapi",
    "uvicorn",
    "pydantic",
    "sqlalchemy",
    "alembic",
    "pytest",
    "black",
    "flake8",
    "mypy",
    "ipython",
    "jupyter",
    "pandas",
    "numpy",
    "anthropic",
    "openai",
    "python-dotenv",
    "typer",
    "rich"
)

foreach ($pkg in $packages) {
    Write-Host "  - Installing $pkg..." -ForegroundColor Gray
    & "$PythonVenv\Scripts\python.exe" -m pip install $pkg --quiet
}

Write-Host "`nPython environment setup complete!" -ForegroundColor Green
Write-Host "Activate with: $PythonVenv\Scripts\Activate.ps1" -ForegroundColor Cyan
