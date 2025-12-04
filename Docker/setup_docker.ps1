# ============================================
# DOCKER CONFIGURATION FOR D:\DevTools
# ============================================

$ErrorActionPreference = "Stop"
$DevTools = "D:\DevTools"
$DockerDir = "$DevTools\Docker"
$DockerData = "$DockerDir\data"
$DockerVolumes = "$DockerDir\volumes"
$DockerCompose = "$DockerDir\compose"

Write-Host "Setting up Docker Environment..." -ForegroundColor Cyan

# Create directories
$dirs = @($DockerData, $DockerVolumes, $DockerCompose)
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Check Docker installation
try {
    $dockerVersion = docker --version
    Write-Host "Found Docker: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker not found. Please install Docker Desktop" -ForegroundColor Red
    exit 1
}

# Check if Docker is running
try {
    docker ps | Out-Null
    Write-Host "Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Docker daemon is not running. Start Docker Desktop first." -ForegroundColor Yellow
}

# Create docker-compose templates
Write-Host "`nCreating Docker Compose templates..." -ForegroundColor Yellow

# PostgreSQL template
$postgresCompose = @"
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    container_name: devtools_postgres
    environment:
      POSTGRES_USER: developer
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: devdb
    ports:
      - "5432:5432"
    volumes:
      - $DockerVolumes/postgres:/var/lib/postgresql/data
    restart: unless-stopped
"@
Set-Content -Path "$DockerCompose\postgres.yml" -Value $postgresCompose

# Redis template
$redisCompose = @"
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    container_name: devtools_redis
    ports:
      - "6379:6379"
    volumes:
      - $DockerVolumes/redis:/data
    restart: unless-stopped
    command: redis-server --appendonly yes
"@
Set-Content -Path "$DockerCompose\redis.yml" -Value $redisCompose

# MongoDB template
$mongoCompose = @"
version: '3.8'
services:
  mongodb:
    image: mongo:7
    container_name: devtools_mongo
    environment:
      MONGO_INITDB_ROOT_USERNAME: developer
      MONGO_INITDB_ROOT_PASSWORD: dev_password
    ports:
      - "27017:27017"
    volumes:
      - $DockerVolumes/mongodb:/data/db
    restart: unless-stopped
"@
Set-Content -Path "$DockerCompose\mongodb.yml" -Value $mongoCompose

# MySQL template
$mysqlCompose = @"
version: '3.8'
services:
  mysql:
    image: mysql:8
    container_name: devtools_mysql
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: devdb
      MYSQL_USER: developer
      MYSQL_PASSWORD: dev_password
    ports:
      - "3306:3306"
    volumes:
      - $DockerVolumes/mysql:/var/lib/mysql
    restart: unless-stopped
"@
Set-Content -Path "$DockerCompose\mysql.yml" -Value $mysqlCompose

# Full stack template
$fullStackCompose = @"
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    container_name: devtools_postgres
    environment:
      POSTGRES_USER: developer
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: devdb
    ports:
      - "5432:5432"
    volumes:
      - $DockerVolumes/postgres:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: devtools_redis
    ports:
      - "6379:6379"
    volumes:
      - $DockerVolumes/redis:/data
    restart: unless-stopped

  mongodb:
    image: mongo:7
    container_name: devtools_mongo
    environment:
      MONGO_INITDB_ROOT_USERNAME: developer
      MONGO_INITDB_ROOT_PASSWORD: dev_password
    ports:
      - "27017:27017"
    volumes:
      - $DockerVolumes/mongodb:/data/db
    restart: unless-stopped
"@
Set-Content -Path "$DockerCompose\fullstack.yml" -Value $fullStackCompose

# Create helper scripts
$startAll = @"
# Start all DevTools containers
Write-Host "Starting all DevTools containers..." -ForegroundColor Cyan
docker-compose -f "$DockerCompose\fullstack.yml" up -d
Write-Host "All containers started!" -ForegroundColor Green
docker ps
"@
Set-Content -Path "$DockerDir\start-all.ps1" -Value $startAll

$stopAll = @"
# Stop all DevTools containers
Write-Host "Stopping all DevTools containers..." -ForegroundColor Yellow
docker-compose -f "$DockerCompose\fullstack.yml" down
Write-Host "All containers stopped!" -ForegroundColor Green
"@
Set-Content -Path "$DockerDir\stop-all.ps1" -Value $stopAll

$status = @"
# Show status of all DevTools containers
Write-Host "DevTools Docker Containers Status:" -ForegroundColor Cyan
docker ps -a --filter "name=devtools_"
"@
Set-Content -Path "$DockerDir\status.ps1" -Value $status

Write-Host "`nDocker environment setup complete!" -ForegroundColor Green
Write-Host "`nAvailable compose files:" -ForegroundColor Cyan
Write-Host "  - postgres.yml  - PostgreSQL database" -ForegroundColor Gray
Write-Host "  - redis.yml     - Redis cache" -ForegroundColor Gray
Write-Host "  - mongodb.yml   - MongoDB database" -ForegroundColor Gray
Write-Host "  - mysql.yml     - MySQL database" -ForegroundColor Gray
Write-Host "  - fullstack.yml - All services" -ForegroundColor Gray
Write-Host "`nQuick commands:" -ForegroundColor Cyan
Write-Host "  - start-all.ps1 - Start all containers" -ForegroundColor Gray
Write-Host "  - stop-all.ps1  - Stop all containers" -ForegroundColor Gray
Write-Host "  - status.ps1    - Show container status" -ForegroundColor Gray
