# Activate venv
& "D:\DevTools\AI\env\Scripts\Activate.ps1"

$python = "D:\DevTools\AI\env\Scripts\python.exe"
$script = "D:\DevTools\AI\scripts\whisper_file.py"

# Audio file path
$audioFile = "D:\DevTools\AI\temp\mic_record.wav"

# Ensure directory exists
$dir = Split-Path $audioFile
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }

Write-Host "Recording 5 seconds from microphone..."

# Use COM-based SoundRecorder on Windows 10
$rec = New-Object -ComObject SoundRecorder.Recorder
$rec.Record()
Start-Sleep -Seconds 5
$rec.Stop()
$rec.SaveFile($audioFile)

Write-Host "Saved audio to: $audioFile"
Write-Host "Running Whisper transcription..."

& $python $script $audioFile
