# ============================================
# GITHUB AUTHENTICATION SETUP
# ============================================

$DevTools = "D:\DevTools"
$CredsFile = "$DevTools\Config\.env"

Write-Host "GitHub Authentication Setup" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan
Write-Host ""

# Check if credentials file exists
if (Test-Path $CredsFile) {
    Write-Host "Loading credentials from .env file..." -ForegroundColor Yellow

    # Parse .env file
    $envContent = Get-Content $CredsFile
    $githubToken = ($envContent | Select-String "GITHUB_TOKEN=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })
    $githubOwner = ($envContent | Select-String "GITHUB_OWNER=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })

    if ($githubToken -and $githubOwner) {
        Write-Host "Found credentials:" -ForegroundColor Green
        Write-Host "  Owner: $githubOwner" -ForegroundColor Gray
        Write-Host "  Token: $($githubToken.Substring(0, 20))..." -ForegroundColor Gray
        Write-Host ""

        # Configure git
        Write-Host "Configuring Git..." -ForegroundColor Yellow
        git config --global user.name "$githubOwner"
        git config --global user.email "$githubOwner@users.noreply.github.com"

        # Setup credential helper
        git config --global credential.helper store

        Write-Host ""
        Write-Host "Git configured successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "To authenticate with GitHub CLI (gh):" -ForegroundColor Cyan
        Write-Host "  echo $githubToken | gh auth login --with-token" -ForegroundColor Gray
        Write-Host ""
        Write-Host "To use token in git operations:" -ForegroundColor Cyan
        Write-Host "  git clone https://$githubOwner:TOKEN@github.com/$githubOwner/repo.git" -ForegroundColor Gray

    } else {
        Write-Host "ERROR: GitHub credentials not found in .env file" -ForegroundColor Red
        Write-Host "Please edit $CredsFile and add:" -ForegroundColor Yellow
        Write-Host "  GITHUB_OWNER=your_username" -ForegroundColor Gray
        Write-Host "  GITHUB_TOKEN=your_token" -ForegroundColor Gray
    }
} else {
    Write-Host "ERROR: .env file not found at $CredsFile" -ForegroundColor Red
    Write-Host "Please create it from env.example" -ForegroundColor Yellow
}
