# Activate venv
& "D:\DevTools\AI\env\Scripts\Activate.ps1"

$python = "D:\DevTools\AI\env\Scripts\python.exe"
$script = "D:\DevTools\AI\scripts\whisper_batch.py"

Write-Host "Starting batch transcription..."
& $python $script
