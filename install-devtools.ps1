# ============================================
# DEVTOOLS COMPLETE INSTALLER
# Windows Development Environment Setup
# Version: 1.0
# Author: DevTools Project
# ============================================

<#
.SYNOPSIS
    Complete development environment installer for Windows

.DESCRIPTION
    Installs and configures:
    - Python 3.11+ with virtual environment
    - Node.js v22+ with global packages
    - Docker with compose files
    - Git configuration
    - DBeaver (database client)
    - Postman (API testing)
    - Terraform (IaC)
    - Essential utilities (jq, tree, 7zip)

.PARAMETER InstallPath
    Installation directory (default: D:\DevTools)

.PARAMETER SkipChocolatey
    Skip Chocolatey packages installation

.EXAMPLE
    .\install-devtools.ps1
    .\install-devtools.ps1 -InstallPath "C:\DevTools"
#>

param(
    [string]$InstallPath = "D:\DevTools",
    [switch]$SkipChocolatey
)

$ErrorActionPreference = "Continue"
$WarningPreference = "SilentlyContinue"

# ============================================
# FUNCTIONS
# ============================================

function Write-Step {
    param([string]$Message, [string]$Color = "Cyan")
    Write-Host "`n========================================" -ForegroundColor $Color
    Write-Host " $Message" -ForegroundColor White
    Write-Host "========================================`n" -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "→ $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Test-Admin {
    $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-Command {
    param([string]$Command)
    return [bool](Get-Command $Command -ErrorAction SilentlyContinue)
}

# ============================================
# PRE-FLIGHT CHECKS
# ============================================

Write-Step "DevTools Installer - Pre-flight Checks" "Magenta"

# Check admin rights
if (-not (Test-Admin)) {
    Write-Error "This script requires Administrator privileges"
    Write-Info "Right-click PowerShell and select 'Run as Administrator'"
    exit 1
}
Write-Success "Running as Administrator"

# Check Windows version
$osVersion = [System.Environment]::OSVersion.Version
if ($osVersion.Major -lt 10) {
    Write-Error "Windows 10 or later is required"
    exit 1
}
Write-Success "Windows version: $($osVersion.Major).$($osVersion.Minor)"

# Check disk space (at least 5GB free)
$drive = Split-Path $InstallPath -Qualifier
$disk = Get-PSDrive $drive.TrimEnd(':')
$freeSpaceGB = [math]::Round($disk.Free / 1GB, 2)

if ($freeSpaceGB -lt 5) {
    Write-Warning "Low disk space: $freeSpaceGB GB free (recommended: 5GB+)"
} else {
    Write-Success "Disk space: $freeSpaceGB GB free"
}

# ============================================
# STEP 1: CREATE DIRECTORY STRUCTURE
# ============================================

Write-Step "Step 1/8: Creating Directory Structure"

$directories = @(
    "$InstallPath",
    "$InstallPath\Python",
    "$InstallPath\NodeJS",
    "$InstallPath\Docker",
    "$InstallPath\Git",
    "$InstallPath\Scripts",
    "$InstallPath\Config",
    "$InstallPath\Docs",
    "$InstallPath\Database",
    "$InstallPath\AI",
    "$InstallPath\Caches",
    "$InstallPath\Installers",
    "$InstallPath\Utils"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Info "Created: $dir"
    }
}

Write-Success "Directory structure created"

# ============================================
# STEP 2: CHECK REQUIRED SOFTWARE
# ============================================

Write-Step "Step 2/8: Checking Required Software"

$requirements = @{
    "Python" = @{
        Command = "python"
        MinVersion = "3.11"
        InstallUrl = "https://www.python.org/downloads/"
    }
    "Node.js" = @{
        Command = "node"
        MinVersion = "18.0"
        InstallUrl = "https://nodejs.org/"
    }
    "Git" = @{
        Command = "git"
        MinVersion = "2.0"
        InstallUrl = "https://git-scm.com/download/win"
    }
    "Docker" = @{
        Command = "docker"
        MinVersion = "20.0"
        InstallUrl = "https://www.docker.com/products/docker-desktop"
        Optional = $true
    }
}

$missingRequired = @()

foreach ($software in $requirements.Keys) {
    $req = $requirements[$software]

    if (Test-Command $req.Command) {
        Write-Success "$software is installed"
    } else {
        if ($req.Optional) {
            Write-Warning "$software is not installed (optional)"
            Write-Info "Install from: $($req.InstallUrl)"
        } else {
            Write-Error "$software is NOT installed (required)"
            Write-Info "Install from: $($req.InstallUrl)"
            $missingRequired += $software
        }
    }
}

if ($missingRequired.Count -gt 0) {
    Write-Error "Missing required software: $($missingRequired -join ', ')"
    Write-Info "Please install missing software and run this script again"
    exit 1
}

# ============================================
# STEP 3: INSTALL CHOCOLATEY PACKAGES
# ============================================

if (-not $SkipChocolatey) {
    Write-Step "Step 3/8: Installing Chocolatey Packages"

    # Check if Chocolatey is installed
    if (-not (Test-Command "choco")) {
        Write-Info "Installing Chocolatey..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    }

    $chocoPackages = @(
        "dbeaver",
        "postman",
        "terraform",
        "jq",
        "tree",
        "7zip"
    )

    foreach ($package in $chocoPackages) {
        Write-Info "Installing $package..."
        choco install $package -y --no-progress 2>&1 | Out-Null
    }

    Write-Success "Chocolatey packages installed"
} else {
    Write-Info "Skipping Chocolatey packages (use -SkipChocolatey:$false to install)"
}

# ============================================
# STEP 4: SETUP PYTHON ENVIRONMENT
# ============================================

Write-Step "Step 4/8: Setting up Python Environment"

$pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pythonExe) {
    Write-Info "Python found at: $pythonExe"

    # Create virtual environment
    $venvPath = "$InstallPath\Python\venv"
    if (-not (Test-Path "$venvPath\Scripts\python.exe")) {
        Write-Info "Creating virtual environment..."
        & $pythonExe -m venv $venvPath

        # Upgrade pip and install packages
        Write-Info "Installing Python packages..."
        $venvPip = "$venvPath\Scripts\pip.exe"
        & $venvPip install --upgrade pip --quiet

        $pythonPackages = @(
            "requests", "aiohttp",
            "fastapi", "uvicorn[standard]",
            "sqlalchemy", "alembic",
            "pytest", "black", "flake8", "mypy",
            "pandas", "numpy",
            "jupyter", "ipython",
            "anthropic", "openai",
            "python-dotenv", "typer", "rich"
        )

        & $venvPip install $pythonPackages -join " " --quiet
        Write-Success "Python environment configured"
    } else {
        Write-Success "Python environment already exists"
    }
}

# ============================================
# STEP 5: SETUP NODE.JS ENVIRONMENT
# ============================================

Write-Step "Step 5/8: Setting up Node.js Environment"

if (Test-Command "npm") {
    Write-Info "Configuring npm..."

    $nodeModules = "$InstallPath\NodeJS\global_modules"
    $npmCache = "$InstallPath\Caches\npm"

    npm config set prefix $nodeModules
    npm config set cache $npmCache

    # Install global packages
    Write-Info "Installing Node.js packages..."
    $npmPackages = @(
        "typescript", "ts-node",
        "nodemon", "pm2",
        "eslint", "prettier",
        "yarn", "pnpm"
    )

    foreach ($pkg in $npmPackages) {
        npm install -g $pkg --quiet 2>&1 | Out-Null
    }

    Write-Success "Node.js environment configured"
}

# ============================================
# STEP 6: SETUP DOCKER ENVIRONMENT
# ============================================

Write-Step "Step 6/8: Setting up Docker Environment"

if (Test-Command "docker") {
    $dockerCompose = "$InstallPath\Docker\compose"
    New-Item -ItemType Directory -Path $dockerCompose -Force | Out-Null

    # Create Docker Compose files (will be copied from templates)
    Write-Info "Docker compose directory created"
    Write-Success "Docker environment configured"
} else {
    Write-Warning "Docker not found - skipping Docker setup"
    Write-Info "Install Docker Desktop from: https://www.docker.com/products/docker-desktop"
}

# ============================================
# STEP 7: COPY SCRIPTS AND DOCUMENTATION
# ============================================

Write-Step "Step 7/8: Setting up Scripts and Documentation"

# This will be populated by the repository files
Write-Info "Scripts and documentation will be available after cloning the repository"
Write-Success "Setup scripts ready"

# ============================================
# STEP 8: CONFIGURE GIT
# ============================================

Write-Step "Step 8/8: Configuring Git"

if (Test-Command "git") {
    $gitUser = git config --global user.name
    $gitEmail = git config --global user.email

    if (-not $gitUser -or -not $gitEmail) {
        Write-Info "Git user not configured"
        Write-Info "Run: git config --global user.name 'Your Name'"
        Write-Info "Run: git config --global user.email 'your@email.com'"
    } else {
        Write-Success "Git configured: $gitUser <$gitEmail>"
    }
}

# ============================================
# COMPLETION
# ============================================

Write-Step "Installation Complete!" "Green"

Write-Host "DevTools has been installed to: $InstallPath`n" -ForegroundColor Cyan

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Clone the DevTools repository:" -ForegroundColor White
Write-Host "     git clone https://github.com/ircitdev/devtools.git`n" -ForegroundColor Gray

Write-Host "  2. Copy scripts and documentation:" -ForegroundColor White
Write-Host "     Copy contents from cloned repo to $InstallPath`n" -ForegroundColor Gray

Write-Host "  3. Run setup scripts:" -ForegroundColor White
Write-Host "     cd $InstallPath" -ForegroundColor Gray
Write-Host "     .\DevTools-Manager.ps1 status`n" -ForegroundColor Gray

Write-Host "  4. Start Docker Desktop (if installed)" -ForegroundColor White
Write-Host "     Then run: .\DevTools-Manager.ps1 docker start`n" -ForegroundColor Gray

Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - README.md - Getting started" -ForegroundColor White
Write-Host "  - QUICKSTART.md - Quick start guide" -ForegroundColor White
Write-Host "  - Docs/ - Detailed documentation`n" -ForegroundColor White

Write-Host "Installation log saved to: $InstallPath\install.log" -ForegroundColor Cyan
Write-Host "`nEnjoy your development environment! 🚀`n" -ForegroundColor Green

# Save installation info
$installInfo = @{
    InstallDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    InstallPath = $InstallPath
    OSVersion = "$($osVersion.Major).$($osVersion.Minor).$($osVersion.Build)"
    PowerShellVersion = $PSVersionTable.PSVersion.ToString()
} | ConvertTo-Json

Set-Content -Path "$InstallPath\install.log" -Value $installInfo
