# Start all DevTools containers
Write-Host "Starting all DevTools containers..." -ForegroundColor Cyan
docker-compose -f "D:\DevTools\Docker\compose\fullstack.yml" up -d
Write-Host "All containers started!" -ForegroundColor Green
docker ps
