# ============================================
# CREATE PYTHON PROJECT FOR VS CODE + CLAUDE
# ============================================

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,

    [Parameter(Mandatory=$false)]
    [ValidateSet("basic", "fastapi", "flask", "data-science", "cli")]
    [string]$Template = "basic"
)

$DevTools = "D:\DevTools"
$ProjectsDir = "$DevTools\Database"
$ProjectPath = "$ProjectsDir\$ProjectName"
$PythonExe = "$DevTools\Python\venv\Scripts\python.exe"

Write-Host "Creating Python Project: $ProjectName" -ForegroundColor Cyan
Write-Host "Template: $Template" -ForegroundColor Gray
Write-Host ""

# Check if project exists
if (Test-Path $ProjectPath) {
    Write-Host "ERROR: Project '$ProjectName' already exists at $ProjectPath" -ForegroundColor Red
    exit 1
}

# Create project directory
Write-Host "[1/10] Creating project structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $ProjectPath -Force | Out-Null
Set-Location $ProjectPath

# Create folder structure
$folders = @("src", "tests", "docs", "scripts", "data")
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
}

# Create virtual environment
Write-Host "[2/10] Creating virtual environment..." -ForegroundColor Yellow
& $PythonExe -m venv .venv

# Activate venv
$venvPython = ".\.venv\Scripts\python.exe"
$venvPip = ".\.venv\Scripts\pip.exe"

# Upgrade pip
Write-Host "[3/10] Upgrading pip..." -ForegroundColor Yellow
& $venvPip install --upgrade pip --quiet

# Create __init__.py files
Write-Host "[4/10] Creating Python modules..." -ForegroundColor Yellow
New-Item -ItemType File "src\__init__.py" -Force | Out-Null
New-Item -ItemType File "tests\__init__.py" -Force | Out-Null

# Create requirements based on template
Write-Host "[5/10] Creating requirements.txt..." -ForegroundColor Yellow

$requirements = switch ($Template) {
    "fastapi" {
        @"
# Web Framework
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.10.5
pydantic-settings==2.7.1

# Database
sqlalchemy==2.0.36
alembic==1.14.0

# HTTP Client
httpx==0.28.1

# Configuration
python-dotenv==1.0.1
"@
    }
    "flask" {
        @"
# Web Framework
flask==3.1.0
flask-sqlalchemy==3.1.1
flask-migrate==4.0.7

# Configuration
python-dotenv==1.0.1

# HTTP Client
requests==2.32.3
"@
    }
    "data-science" {
        @"
# Data Analysis
pandas==2.3.0
numpy==2.3.0
matplotlib==3.10.0
seaborn==0.13.2

# Machine Learning
scikit-learn==1.6.1

# Jupyter
jupyter==1.1.1
ipykernel==6.30.2

# Configuration
python-dotenv==1.0.1
"@
    }
    "cli" {
        @"
# CLI Framework
typer[all]==0.15.1
rich==13.9.4
click==8.1.8

# Configuration
python-dotenv==1.0.1
"@
    }
    default {
        @"
# Core
python-dotenv==1.0.1
requests==2.32.3
"@
    }
}

Set-Content -Path "requirements.txt" -Value $requirements

# Create requirements-dev.txt
$requirementsDev = @"
# Include production dependencies
-r requirements.txt

# Testing
pytest==8.3.4
pytest-cov==6.0.0

# Linting and Formatting
black==25.3.0
flake8==7.1.1
mypy==1.14.1

# Tools
ipython==8.31.0
"@
Set-Content -Path "requirements-dev.txt" -Value $requirementsDev

# Install dependencies
Write-Host "[6/10] Installing dependencies..." -ForegroundColor Yellow
& $venvPip install -r requirements-dev.txt --quiet

# Create main.py based on template
Write-Host "[7/10] Creating source files..." -ForegroundColor Yellow

$mainPy = switch ($Template) {
    "fastapi" {
        @"
"""FastAPI application."""
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "$ProjectName"),
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Hello from $ProjectName!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
"@
    }
    "flask" {
        @"
"""Flask application."""
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def root():
    return {"message": "Hello from $ProjectName!"}

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
"@
    }
    "data-science" {
        @"
"""Data science utilities."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main function."""
    print("Data Science Project: $ProjectName")

    # Example: Create sample data
    df = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100)
    })

    print(f"Created DataFrame with {len(df)} rows")
    print(df.describe())

if __name__ == "__main__":
    main()
"@
    }
    "cli" {
        @"
"""CLI application."""
import typer
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()
console = Console()

@app.command()
def hello(name: str):
    \"\"\"Say hello to someone.\"\"\"
    console.print(f"Hello {name}!", style="bold green")

@app.command()
def goodbye(name: str):
    \"\"\"Say goodbye to someone.\"\"\"
    console.print(f"Goodbye {name}!", style="bold red")

if __name__ == "__main__":
    app()
"@
    }
    default {
        @"
"""Main application module."""
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    \"\"\"Main function.\"\"\"
    print(f"Hello from {os.getenv('APP_NAME', '$ProjectName')}!")

if __name__ == "__main__":
    main()
"@
    }
}

Set-Content -Path "src\main.py" -Value $mainPy -Encoding UTF8

# Create test file
$testMain = @"
"""Tests for main module."""
import pytest
from src.main import main

def test_main():
    \"\"\"Test main function.\"\"\"
    # Add your tests here
    assert True
"@
Set-Content -Path "tests\test_main.py" -Value $testMain -Encoding UTF8

# Create VS Code settings
Write-Host "[8/10] Creating VS Code configuration..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path ".vscode" -Force | Out-Null

$settingsJson = @"
{
  "python.defaultInterpreterPath": "`${workspaceFolder}/.venv/Scripts/python.exe",
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.analysis.autoImportCompletions": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true,
    ".mypy_cache": true
  }
}
"@
Set-Content -Path ".vscode\settings.json" -Value $settingsJson

$launchJson = @"
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "`${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Main",
      "type": "debugpy",
      "request": "launch",
      "program": "`${workspaceFolder}/src/main.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
"@
Set-Content -Path ".vscode\launch.json" -Value $launchJson

# Create .gitignore
Write-Host "[9/10] Creating .gitignore..." -ForegroundColor Yellow
$gitignore = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Mypy
.mypy_cache/

# Environment
.env
.env.local

# Database
*.db
*.sqlite3

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Distribution
dist/
build/
*.egg-info/
"@
Set-Content -Path ".gitignore" -Value $gitignore

# Create .env.example
$envExample = @"
# Application
APP_NAME=$ProjectName
APP_ENV=development
DEBUG=True

# Database (if needed)
DATABASE_URL=postgresql://developer:dev_password@localhost:5432/devdb

# API Keys
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
"@
Set-Content -Path ".env.example" -Value $envExample

# Create README
$readme = @"
# $ProjectName

Created with DevTools Python Project Generator

## Setup

1. Activate virtual environment:
``````powershell
.\.venv\Scripts\activate.ps1
``````

2. Install dependencies:
``````bash
pip install -r requirements-dev.txt
``````

## Usage

``````bash
python src/main.py
``````

## Testing

``````bash
pytest
``````

## Development

- Format code: ``black src tests``
- Lint code: ``flake8 src tests``
- Type check: ``mypy src``
"@
Set-Content -Path "README.md" -Value $readme

# Initialize Git
Write-Host "[10/10] Initializing Git..." -ForegroundColor Yellow
git init | Out-Null
git add . | Out-Null
git commit -m "Initial commit: $ProjectName" | Out-Null

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   PROJECT CREATED SUCCESSFULLY!" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Project: $ProjectName" -ForegroundColor Cyan
Write-Host "Location: $ProjectPath" -ForegroundColor Cyan
Write-Host "Template: $Template" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. cd $ProjectPath" -ForegroundColor Gray
Write-Host "  2. code ." -ForegroundColor Gray
Write-Host "  3. Activate venv: .\.venv\Scripts\activate.ps1" -ForegroundColor Gray
Write-Host "  4. Run: python src\main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "VS Code:" -ForegroundColor Yellow
Write-Host "  - Press F5 to debug" -ForegroundColor Gray
Write-Host "  - Use Claude Code for assistance" -ForegroundColor Gray
Write-Host "  - Run tests from Testing panel" -ForegroundColor Gray
Write-Host ""
