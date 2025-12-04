# ============================================
# START JUPYTER LAB (Modern Interface)
# ============================================

$DevTools = "D:\DevTools"
$PythonVenv = "$DevTools\Python\venv\Scripts\python.exe"
$JupyterExe = "$DevTools\Python\venv\Scripts\jupyter.exe"

Write-Host "Starting JupyterLab..." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $JupyterExe)) {
    Write-Host "ERROR: Jupyter not found. Installing..." -ForegroundColor Yellow
    & $PythonVenv -m pip install jupyterlab --quiet
}

Write-Host "JupyterLab will open in your browser" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start JupyterLab in current directory or DevTools
$startDir = Get-Location
if ($startDir -eq "D:\") {
    Set-Location "$DevTools\Database"
}

& $JupyterExe lab
