# Quick Python Activation Script
$VenvPath = "D:\DevTools\Python\venv\Scripts\Activate.ps1"

if (Test-Path $VenvPath) {
    & $VenvPath
    Write-Host "Python environment activated!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Python venv not found. Run setup_python.ps1 first" -ForegroundColor Red
}
