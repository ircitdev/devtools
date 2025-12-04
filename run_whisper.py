# Activate venv
& "D:\DevTools\AI\env\Scripts\Activate.ps1"

$python = "D:\DevTools\AI\env\Scripts\python.exe"
$script = "D:\DevTools\AI\scripts\run_whisper.py"

Write-Host "Running Whisper..." -ForegroundColor Cyan

& $python $script
