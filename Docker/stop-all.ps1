# Stop all DevTools containers
Write-Host "Stopping all DevTools containers..." -ForegroundColor Yellow
docker-compose -f "D:\DevTools\Docker\compose\fullstack.yml" down
Write-Host "All containers stopped!" -ForegroundColor Green
