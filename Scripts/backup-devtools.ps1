# ============================================
# BACKUP DEVTOOLS ENVIRONMENT
# ============================================

$DevTools = "D:\DevTools"
$BackupDir = "D:\Backups"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupName = "DevTools_Backup_$Timestamp.zip"
$BackupPath = "$BackupDir\$BackupName"

Write-Host "DevTools Backup Utility" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Create backup directory
if (-not (Test-Path $BackupDir)) {
    Write-Host "Creating backup directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

Write-Host "Creating backup..." -ForegroundColor Yellow
Write-Host "Source: $DevTools" -ForegroundColor Gray
Write-Host "Destination: $BackupPath" -ForegroundColor Gray
Write-Host ""

# Exclude large/temporary directories
$ExcludeDirs = @(
    "Temp",
    "Caches",
    "LM Studio",
    "Python\venv\Lib",
    "NodeJS\global_modules\node_modules",
    "Docker\volumes"
)

Write-Host "Excluding:" -ForegroundColor Yellow
foreach ($dir in $ExcludeDirs) {
    Write-Host "  - $dir" -ForegroundColor Gray
}
Write-Host ""

# Create archive (without excluded dirs)
try {
    $compress = @{
        Path = "$DevTools\*.ps1", "$DevTools\*.md", "$DevTools\Python\*.ps1", "$DevTools\NodeJS\*.ps1",
               "$DevTools\Docker\*.ps1", "$DevTools\Git\*.ps1", "$DevTools\Scripts\*.ps1",
               "$DevTools\Config\*", "$DevTools\AI\*.ps1"
        DestinationPath = $BackupPath
        CompressionLevel = "Optimal"
    }

    Compress-Archive @compress -Force

    $size = (Get-Item $BackupPath).Length / 1MB

    Write-Host ""
    Write-Host "Backup completed successfully!" -ForegroundColor Green
    Write-Host "Location: $BackupPath" -ForegroundColor Cyan
    Write-Host "Size: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To restore, extract this archive to D:\" -ForegroundColor Yellow

} catch {
    Write-Host "ERROR: Backup failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
