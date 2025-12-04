# ============================================
# GIT CONFIGURATION FOR D:\DevTools
# ============================================

$ErrorActionPreference = "Stop"
$DevTools = "D:\DevTools"
$GitDir = "$DevTools\Git"
$GitConfig = "$GitDir\config"

Write-Host "Setting up Git Environment..." -ForegroundColor Cyan

# Create directories
if (-not (Test-Path $GitConfig)) {
    New-Item -ItemType Directory -Path $GitConfig -Force | Out-Null
}

# Check Git installation
try {
    $gitVersion = git --version
    Write-Host "Found Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git not found in PATH" -ForegroundColor Red
    exit 1
}

# Create .gitconfig template
$gitConfigTemplate = @"
[user]
    name = Your Name
    email = your.email@example.com

[core]
    autocrlf = true
    editor = code --wait

[init]
    defaultBranch = main

[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    cm = commit -m
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    last = log -1 HEAD
    unstage = reset HEAD --
    amend = commit --amend

[pull]
    rebase = false

[push]
    default = simple

[fetch]
    prune = true

[diff]
    tool = vscode

[difftool "vscode"]
    cmd = code --wait --diff $LOCAL $REMOTE

[merge]
    tool = vscode

[mergetool "vscode"]
    cmd = code --wait $MERGED
"@
Set-Content -Path "$GitConfig\.gitconfig" -Value $gitConfigTemplate

# Create .gitignore template
$gitIgnoreTemplate = @"
# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Dependencies
node_modules/
vendor/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Build outputs
dist/
build/
*.exe
*.dll
*.so
*.dylib

# Environment
.env
.env.local
.env.*.local

# Temporary
tmp/
temp/
*.tmp
*.bak
*.cache

# Package managers
package-lock.json
yarn.lock
composer.lock
"@
Set-Content -Path "$GitConfig\.gitignore" -Value $gitIgnoreTemplate

# Create helper scripts
$setupUser = @"
# Setup Git User Configuration
Write-Host "Git User Configuration" -ForegroundColor Cyan
Write-Host ""

`$name = Read-Host "Enter your name"
`$email = Read-Host "Enter your email"

git config --global user.name "`$name"
git config --global user.email "`$email"

Write-Host ""
Write-Host "Git user configured:" -ForegroundColor Green
Write-Host "Name:  `$name" -ForegroundColor Gray
Write-Host "Email: `$email" -ForegroundColor Gray
"@
Set-Content -Path "$GitDir\setup-user.ps1" -Value $setupUser

$showConfig = @"
# Show current Git configuration
Write-Host "Current Git Configuration:" -ForegroundColor Cyan
Write-Host ""
git config --list --show-origin
"@
Set-Content -Path "$GitDir\show-config.ps1" -Value $showConfig

Write-Host "`nGit environment setup complete!" -ForegroundColor Green
Write-Host "`nConfiguration files:" -ForegroundColor Cyan
Write-Host "  - .gitconfig  - Git configuration template" -ForegroundColor Gray
Write-Host "  - .gitignore  - Default ignore patterns" -ForegroundColor Gray
Write-Host "`nHelper scripts:" -ForegroundColor Cyan
Write-Host "  - setup-user.ps1  - Configure Git user" -ForegroundColor Gray
Write-Host "  - show-config.ps1 - Show Git configuration" -ForegroundColor Gray
Write-Host "`nRun setup-user.ps1 to configure your Git identity" -ForegroundColor Yellow
