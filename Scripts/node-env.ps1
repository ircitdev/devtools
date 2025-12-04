# ============================================
# NODE.JS ENVIRONMENT ACTIVATOR
# ============================================

$DevTools = "D:\DevTools"
$NodeModules = "$DevTools\NodeJS\global_modules"

Write-Host "Activating Node.js Environment..." -ForegroundColor Cyan

# Add to PATH for current session
$env:PATH = "$NodeModules;$env:PATH"
$env:NPM_CONFIG_PREFIX = $NodeModules

Write-Host "Node.js environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Yellow
Write-Host "  typescript - tsc, ts-node" -ForegroundColor Gray
Write-Host "  nodemon    - Auto-restart Node apps" -ForegroundColor Gray
Write-Host "  pm2        - Process manager" -ForegroundColor Gray
Write-Host "  eslint     - JavaScript linter" -ForegroundColor Gray
Write-Host "  prettier   - Code formatter" -ForegroundColor Gray
Write-Host "  yarn/pnpm  - Package managers" -ForegroundColor Gray
Write-Host ""
Write-Host "Test with: tsc --version" -ForegroundColor Cyan
