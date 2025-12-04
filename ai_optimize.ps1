Write-Host "AI CPU BOOST: enabling High performance power plan..." -ForegroundColor Cyan

# Set High Performance power plan
$schemeHigh = "SCHEME_MIN"
powercfg -setactive $schemeHigh

Write-Host "Done. Current power scheme set to HIGH PERFORMANCE." -ForegroundColor Green

# Optional: disable some visual effects (minimal)
Write-Host "Tweaking visual effects for performance..."
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f | Out-Null
