# ============================================
# DEVTOOLS MASTER MANAGER
# D:\DevTools - Unified Development Environment
# ============================================

param(
    [Parameter(Position=0)]
    [ValidateSet("setup", "status", "activate", "docker", "help")]
    [string]$Command = "help",

    [Parameter(Position=1)]
    [string]$SubCommand = ""
)

$DevTools = "D:\DevTools"
$ErrorActionPreference = "Stop"

function Show-Banner {
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "   DEVTOOLS MANAGER v1.0" -ForegroundColor White
    Write-Host "   Portable Development Environment" -ForegroundColor Gray
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Show-Banner
    Write-Host "Usage: .\DevTools-Manager.ps1 <command> [subcommand]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Cyan
    Write-Host "  setup <tool>    - Setup development tools" -ForegroundColor White
    Write-Host "    python        - Setup Python environment" -ForegroundColor Gray
    Write-Host "    nodejs        - Setup Node.js environment" -ForegroundColor Gray
    Write-Host "    docker        - Setup Docker containers" -ForegroundColor Gray
    Write-Host "    git           - Setup Git configuration" -ForegroundColor Gray
    Write-Host "    all           - Setup everything" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  status          - Show status of all tools" -ForegroundColor White
    Write-Host ""
    Write-Host "  activate <env>  - Activate environment" -ForegroundColor White
    Write-Host "    python        - Activate Python venv" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  docker <cmd>    - Docker commands" -ForegroundColor White
    Write-Host "    start         - Start all containers" -ForegroundColor Gray
    Write-Host "    stop          - Stop all containers" -ForegroundColor Gray
    Write-Host "    status        - Show container status" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  help            - Show this help" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\DevTools-Manager.ps1 setup all" -ForegroundColor Gray
    Write-Host "  .\DevTools-Manager.ps1 activate python" -ForegroundColor Gray
    Write-Host "  .\DevTools-Manager.ps1 docker start" -ForegroundColor Gray
    Write-Host ""
}

function Show-Status {
    Show-Banner
    Write-Host "Environment Status:" -ForegroundColor Cyan
    Write-Host ""

    # Python
    Write-Host "[Python]" -ForegroundColor Yellow
    if (Test-Path "$DevTools\Python\venv\Scripts\python.exe") {
        $pyVer = & "$DevTools\Python\venv\Scripts\python.exe" --version 2>&1
        Write-Host "  Status: Configured" -ForegroundColor Green
        Write-Host "  Version: $pyVer" -ForegroundColor Gray
        Write-Host "  Path: $DevTools\Python\venv" -ForegroundColor Gray
    } else {
        Write-Host "  Status: Not configured" -ForegroundColor Red
        Write-Host "  Run: .\DevTools-Manager.ps1 setup python" -ForegroundColor Yellow
    }
    Write-Host ""

    # Node.js
    Write-Host "[Node.js]" -ForegroundColor Yellow
    try {
        $nodeVer = node --version 2>&1
        $npmVer = npm --version 2>&1
        Write-Host "  Status: Installed" -ForegroundColor Green
        Write-Host "  Node: $nodeVer" -ForegroundColor Gray
        Write-Host "  npm: $npmVer" -ForegroundColor Gray
    } catch {
        Write-Host "  Status: Not found in PATH" -ForegroundColor Red
    }
    Write-Host ""

    # Git
    Write-Host "[Git]" -ForegroundColor Yellow
    try {
        $gitVer = git --version 2>&1
        Write-Host "  Status: Installed" -ForegroundColor Green
        Write-Host "  Version: $gitVer" -ForegroundColor Gray
        $gitUser = git config --global user.name 2>&1
        $gitEmail = git config --global user.email 2>&1
        if ($gitUser) {
            Write-Host "  User: $gitUser <$gitEmail>" -ForegroundColor Gray
        } else {
            Write-Host "  User: Not configured" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  Status: Not found in PATH" -ForegroundColor Red
    }
    Write-Host ""

    # Docker
    Write-Host "[Docker]" -ForegroundColor Yellow
    try {
        $dockerVer = docker --version 2>&1
        Write-Host "  Status: Installed" -ForegroundColor Green
        Write-Host "  Version: $dockerVer" -ForegroundColor Gray
        try {
            $containers = docker ps -a --filter "name=devtools_" --format "{{.Names}}" 2>&1
            if ($containers) {
                Write-Host "  Containers: $($containers -split "`n" | Measure-Object).Count" -ForegroundColor Gray
            } else {
                Write-Host "  Containers: None" -ForegroundColor Gray
            }
        } catch {
            Write-Host "  Daemon: Not running" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  Status: Not found in PATH" -ForegroundColor Red
    }
    Write-Host ""

    # VSCode
    Write-Host "[VSCode]" -ForegroundColor Yellow
    try {
        $codeVer = code --version 2>&1 | Select-Object -First 1
        Write-Host "  Status: Installed" -ForegroundColor Green
        Write-Host "  Version: $codeVer" -ForegroundColor Gray
    } catch {
        Write-Host "  Status: Not found in PATH" -ForegroundColor Red
    }
    Write-Host ""
}

function Setup-Tool {
    param([string]$Tool)

    Show-Banner

    switch ($Tool.ToLower()) {
        "python" {
            Write-Host "Setting up Python environment..." -ForegroundColor Cyan
            & "$DevTools\Python\setup_python.ps1"
        }
        "nodejs" {
            Write-Host "Setting up Node.js environment..." -ForegroundColor Cyan
            & "$DevTools\NodeJS\setup_nodejs.ps1"
        }
        "docker" {
            Write-Host "Setting up Docker environment..." -ForegroundColor Cyan
            & "$DevTools\Docker\setup_docker.ps1"
        }
        "git" {
            Write-Host "Setting up Git configuration..." -ForegroundColor Cyan
            & "$DevTools\Git\setup_git.ps1"
        }
        "all" {
            Write-Host "Setting up ALL environments..." -ForegroundColor Cyan
            Write-Host ""
            & "$DevTools\Python\setup_python.ps1"
            Write-Host "`n----------------------------------------`n"
            & "$DevTools\NodeJS\setup_nodejs.ps1"
            Write-Host "`n----------------------------------------`n"
            & "$DevTools\Docker\setup_docker.ps1"
            Write-Host "`n----------------------------------------`n"
            & "$DevTools\Git\setup_git.ps1"
            Write-Host "`n"
            Write-Host "============================================" -ForegroundColor Green
            Write-Host "   ALL TOOLS CONFIGURED!" -ForegroundColor White
            Write-Host "============================================" -ForegroundColor Green
        }
        default {
            Write-Host "ERROR: Unknown tool '$Tool'" -ForegroundColor Red
            Write-Host "Available: python, nodejs, docker, git, all" -ForegroundColor Yellow
        }
    }
}

function Activate-Environment {
    param([string]$Env)

    switch ($Env.ToLower()) {
        "python" {
            if (Test-Path "$DevTools\Python\venv\Scripts\Activate.ps1") {
                Write-Host "Activating Python environment..." -ForegroundColor Cyan
                & "$DevTools\Python\venv\Scripts\Activate.ps1"
            } else {
                Write-Host "ERROR: Python venv not found. Run setup first." -ForegroundColor Red
            }
        }
        default {
            Write-Host "ERROR: Unknown environment '$Env'" -ForegroundColor Red
            Write-Host "Available: python" -ForegroundColor Yellow
        }
    }
}

function Docker-Command {
    param([string]$Cmd)

    switch ($Cmd.ToLower()) {
        "start" {
            if (Test-Path "$DevTools\Docker\start-all.ps1") {
                & "$DevTools\Docker\start-all.ps1"
            } else {
                Write-Host "ERROR: Docker not configured. Run setup first." -ForegroundColor Red
            }
        }
        "stop" {
            if (Test-Path "$DevTools\Docker\stop-all.ps1") {
                & "$DevTools\Docker\stop-all.ps1"
            } else {
                Write-Host "ERROR: Docker not configured. Run setup first." -ForegroundColor Red
            }
        }
        "status" {
            if (Test-Path "$DevTools\Docker\status.ps1") {
                & "$DevTools\Docker\status.ps1"
            } else {
                Write-Host "ERROR: Docker not configured. Run setup first." -ForegroundColor Red
            }
        }
        default {
            Write-Host "ERROR: Unknown docker command '$Cmd'" -ForegroundColor Red
            Write-Host "Available: start, stop, status" -ForegroundColor Yellow
        }
    }
}

# Main execution
switch ($Command.ToLower()) {
    "setup" {
        if ($SubCommand) {
            Setup-Tool $SubCommand
        } else {
            Write-Host "ERROR: Specify what to setup" -ForegroundColor Red
            Write-Host "Usage: .\DevTools-Manager.ps1 setup <python|nodejs|docker|git|all>" -ForegroundColor Yellow
        }
    }
    "status" {
        Show-Status
    }
    "activate" {
        if ($SubCommand) {
            Activate-Environment $SubCommand
        } else {
            Write-Host "ERROR: Specify what to activate" -ForegroundColor Red
            Write-Host "Usage: .\DevTools-Manager.ps1 activate <python>" -ForegroundColor Yellow
        }
    }
    "docker" {
        if ($SubCommand) {
            Docker-Command $SubCommand
        } else {
            Write-Host "ERROR: Specify docker command" -ForegroundColor Red
            Write-Host "Usage: .\DevTools-Manager.ps1 docker <start|stop|status>" -ForegroundColor Yellow
        }
    }
    "help" {
        Show-Help
    }
    default {
        Show-Help
    }
}
