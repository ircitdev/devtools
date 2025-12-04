# ============================================
# START JUPYTER NOTEBOOK
# ============================================

$DevTools = "D:\DevTools"
$PythonVenv = "$DevTools\Python\venv\Scripts\python.exe"
$JupyterExe = "$DevTools\Python\venv\Scripts\jupyter.exe"

Write-Host "Starting Jupyter Notebook..." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $JupyterExe)) {
    Write-Host "ERROR: Jupyter not found. Installing..." -ForegroundColor Yellow
    & $PythonVenv -m pip install jupyter --quiet
}

Write-Host "Jupyter will open in your browser" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start Jupyter in current directory or DevTools
$startDir = Get-Location
if ($startDir -eq "D:\") {
    Set-Location "$DevTools\Database"
}

& $JupyterExe notebook
