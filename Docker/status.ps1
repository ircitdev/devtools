# Show status of all DevTools containers
Write-Host "DevTools Docker Containers Status:" -ForegroundColor Cyan
docker ps -a --filter "name=devtools_"
