# ============================================
# AI FULL INSTALLER (CPU ONLY, CLEAN VERSION)
# Windows 10 + GTX 960 + D:\DevTools\AI
# ============================================

Write-Host "AI FULL INSTALLER (CPU ONLY)" -ForegroundColor Cyan

# ---- CHECK ADMIN ----

$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "ERROR: Run PowerShell as Administrator." -ForegroundColor Red
    exit 1
}

# ---- PATHS ----

$DevRoot   = "D:\DevTools"
$AiRoot    = "$DevRoot\AI"
$AiEnvPath = "$AiRoot\env"
$AiTemp    = "$AiRoot\temp"
$AiLogs    = "$AiRoot\logs"
$InstallersDir = "$DevRoot\Installers"

$dirs = @($DevRoot,$AiRoot,$AiEnvPath,$AiTemp,$AiLogs,$InstallersDir)
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null }
}

$env:TEMP = $AiTemp
$env:TMP  = $AiTemp

# ---- LOG FUNCTION ----

$logFile = "$AiLogs\ai_install_$(Get-Date -Format yyyyMMdd_HHmmss).log"

function Log($msg) {
    $t = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$t $msg" | Out-File -FilePath $logFile -Append -Encoding utf8
}

Log "AI INSTALLER STARTED"

# ---- HELPERS ----

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-PyVer {
    if (Test-Command "python") {
        try {
            $v = (& python --version 2>&1)
            return ($v -replace '[^\d\.]', '')
        } catch { return $null }
    }
    return $null
}

# ---- CHECK PYTHON ----

Write-Host "`nChecking Python..." -ForegroundColor Cyan
$pyVer = Get-PyVer

if (-not $pyVer) {
    Write-Host "Python is NOT installed. Install Python 3.11+ first." -ForegroundColor Red
    Log "Python not found."
    exit 1
}

Write-Host "Python found: $pyVer" -ForegroundColor Green
Log "Python = $pyVer"

# ---- VENV ----

$venvPython = "$AiEnvPath\Scripts\python.exe"

if (Test-Path $venvPython) {
    Write-Host "Venv already exists." -ForegroundColor Green
    Log "Venv exists."
} else {
    Write-Host "Creating venv..." -ForegroundColor Yellow
    Log "Creating venv."

    try {
        python -m venv $AiEnvPath
    } catch {
        Write-Host "Failed to create venv." -ForegroundColor Red
        Log "ERROR: venv create fail."
        exit 1
    }
}

if (-not (Test-Path $venvPython)) {
    Write-Host "Venv python not found. Abort." -ForegroundColor Red
    Log "Venv python missing."
    exit 1
}

Write-Host "Using venv python: $venvPython" -ForegroundColor Cyan

# ---- UPGRADE PIP ----

Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
Log "pip upgrade"
try {
    & $venvPython -m pip install --upgrade pip setuptools wheel
} catch {
    Write-Host "pip upgrade failed." -ForegroundColor Red
}

# ---- INSTALL TORCH (CPU) ----

Write-Host "`nInstalling PyTorch CPU..." -ForegroundColor Yellow
Log "Install torch CPU"

try {
    & $venvPython -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
} catch {
    Write-Host "ERROR installing torch." -ForegroundColor Red
}

# ---- INSTALL TENSORFLOW CPU ----

Write-Host "`nInstalling TensorFlow CPU..." -ForegroundColor Yellow
Log "Install tensorflow CPU"

try {
    & $venvPython -m pip install tensorflow
} catch {
    Write-Host "ERROR installing TensorFlow." -ForegroundColor Red
}

# ---- INSTALL ONNX ----

Write-Host "`nInstalling ONNX Runtime..." -ForegroundColor Yellow
Log "Install onnx"

try {
    & $venvPython -m pip install onnx onnxruntime onnxruntime-tools
} catch {
    Write-Host "ERROR installing ONNX." -ForegroundColor Red
}

# ---- INSTALL TRANSFORMERS ----

Write-Host "`nInstalling transformers stack..." -ForegroundColor Yellow
Log "Install transformers"

try {
    & $venvPython -m pip install transformers accelerate sentencepiece safetensors
} catch {
    Write-Host "ERROR installing transformers." -ForegroundColor Red
}

# ---- INSTALL WHISPER ----

Write-Host "`nInstalling openai-whisper..." -ForegroundColor Yellow
Log "Install whisper"

try {
    & $venvPython -m pip install openai-whisper
} catch {
    Write-Host "ERROR installing whisper." -ForegroundColor Red
}

# ---- INSTALL LLAMA-CPP-PYTHON ----

Write-Host "`nInstalling llama-cpp-python..." -ForegroundColor Yellow
Log "Install llama-cpp-python"

try {
    & $venvPython -m pip install llama-cpp-python
} catch {
    Write-Host "ERROR installing llama-cpp-python." -ForegroundColor Red
}

# ---- INSTALL BASE SCIENTIFIC ----

Write-Host "`nInstalling scientific stack..." -ForegroundColor Yellow
Log "Install numpy/scipy/pandas"

try {
    & $venvPython -m pip install numpy scipy pandas rich typer
} catch {
    Write-Host "ERROR installing scientific stack." -ForegroundColor Red
}

# ---- QUICK TEST ----

Write-Host "`nRunning quick import test..." -ForegroundColor Cyan

$testScript = @"
import torch, tensorflow, onnxruntime, transformers, whisper, llama_cpp
print("All core AI libraries imported OK.")
"@

try {
    & $venvPython -c $testScript
    Write-Host "Quick test OK." -ForegroundColor Green
    Log "Quick test OK."
} catch {
    Write-Host "Quick test failed (see log)." -ForegroundColor Yellow
    Log "Quick test ERROR."
}

# ---- OPEN OLLAMA / LM STUDIO DOWNLOAD PAGES ----

Write-Host "`nOpening download pages for Ollama and LM Studio..." -ForegroundColor Cyan
Log "Open browser pages"

Start-Process "https://ollama.com/download/windows"
Start-Process "https://lmstudio.ai/download"

# ---- FINISH ----

Write-Host "`n========================================="
Write-Host " AI INSTALLER COMPLETE "
Write-Host " Venv: $AiEnvPath"
Write-Host " Activate with:"
Write-Host "   $AiEnvPath\Scripts\Activate.ps1"
Write-Host "========================================="

Log "AI INSTALLER FINISHED"
