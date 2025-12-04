# Quick pip Launcher
$DevTools = "D:\DevTools"
$PythonVenv = "$DevTools\Python\venv\Scripts\python.exe"

if (Test-Path $PythonVenv) {
    & $PythonVenv -m pip $args
} else {
    Write-Host "ERROR: Python venv not found. Run setup first." -ForegroundColor Red
}
