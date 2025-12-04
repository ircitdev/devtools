# Quick Python Launcher
$DevTools = "D:\DevTools"
$PythonVenv = "$DevTools\Python\venv\Scripts\python.exe"

if (Test-Path $PythonVenv) {
    if ($args.Count -gt 0) {
        & $PythonVenv $args
    } else {
        & $PythonVenv
    }
} else {
    Write-Host "ERROR: Python venv not found. Run setup first." -ForegroundColor Red
    Write-Host ".\DevTools-Manager.ps1 setup python" -ForegroundColor Yellow
}
