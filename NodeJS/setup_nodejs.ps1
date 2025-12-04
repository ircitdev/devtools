# ============================================
# PORTABLE NODE.JS SETUP FOR D:\DevTools
# ============================================

$ErrorActionPreference = "Stop"
$DevTools = "D:\DevTools"
$NodeDir = "$DevTools\NodeJS"
$NodeModules = "$NodeDir\global_modules"
$NodeCache = "$DevTools\Caches\npm"

Write-Host "Setting up Portable Node.js Environment..." -ForegroundColor Cyan

# Create directories
$dirs = @($NodeModules, $NodeCache)
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Check Node.js installation
$nodeExe = (Get-Command node -ErrorAction SilentlyContinue).Source
if (-not $nodeExe) {
    Write-Host "ERROR: Node.js not found in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Found Node.js: $nodeExe" -ForegroundColor Green
Write-Host "Version: $(node --version)" -ForegroundColor Green
Write-Host "npm version: $(npm --version)" -ForegroundColor Green

# Configure npm to use DevTools directories
Write-Host "`nConfiguring npm for portable use..." -ForegroundColor Yellow

npm config set prefix $NodeModules
npm config set cache $NodeCache

# Create .npmrc in NodeJS directory
$npmrcContent = @"
prefix=$NodeModules
cache=$NodeCache
"@
Set-Content -Path "$NodeDir\.npmrc" -Value $npmrcContent

Write-Host "npm configured for portable use" -ForegroundColor Green

# Install essential global packages
Write-Host "`nInstalling essential global packages..." -ForegroundColor Yellow
$globalPackages = @(
    "typescript",
    "ts-node",
    "nodemon",
    "pm2",
    "http-server",
    "eslint",
    "prettier",
    "yarn",
    "pnpm"
)

foreach ($pkg in $globalPackages) {
    Write-Host "  - Installing $pkg..." -ForegroundColor Gray
    npm install -g $pkg --quiet 2>&1 | Out-Null
}

Write-Host "`nNode.js environment setup complete!" -ForegroundColor Green
Write-Host "Global modules: $NodeModules" -ForegroundColor Cyan
Write-Host "Add to PATH: $NodeModules" -ForegroundColor Yellow
