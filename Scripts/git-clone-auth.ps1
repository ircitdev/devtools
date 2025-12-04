# ============================================
# GIT CLONE WITH AUTHENTICATION
# ============================================

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoName,

    [Parameter(Mandatory=$false)]
    [string]$DestPath = "."
)

$DevTools = "D:\DevTools"
$CredsFile = "$DevTools\Config\.env"

Write-Host "Git Clone with Authentication" -ForegroundColor Cyan
Write-Host ""

# Load credentials
if (-not (Test-Path $CredsFile)) {
    Write-Host "ERROR: Credentials file not found: $CredsFile" -ForegroundColor Red
    exit 1
}

$envContent = Get-Content $CredsFile
$githubToken = ($envContent | Select-String "GITHUB_TOKEN=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })
$githubOwner = ($envContent | Select-String "GITHUB_OWNER=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })

if (-not $githubToken -or -not $githubOwner) {
    Write-Host "ERROR: GitHub credentials not found in .env" -ForegroundColor Red
    exit 1
}

# Build clone URL
$cloneUrl = "https://$githubOwner:$githubToken@github.com/$githubOwner/$RepoName.git"

Write-Host "Cloning repository..." -ForegroundColor Yellow
Write-Host "  Repository: $githubOwner/$RepoName" -ForegroundColor Gray
Write-Host "  Destination: $DestPath" -ForegroundColor Gray
Write-Host ""

try {
    git clone $cloneUrl $DestPath
    Write-Host ""
    Write-Host "Repository cloned successfully!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to clone repository" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
