<#
    Windows 10 DEV/AI PRO Smart Installer
    D:\DevTools edition

    Цели:
    - Минимизировать использование диска C:\
    - Скачивать инсталляторы и хранить кэши на D:\DevTools
    - Устанавливать только то, чего нет, остальное — аккуратно пропускать
#>

Write-Host "🚀 Windows 10 DEV/AI PRO Smart Installer (D:\DevTools edition)" -ForegroundColor Cyan

# ---------- БАЗОВЫЕ НАСТРОЙКИ ПУТЕЙ ----------

$DevRoot      = "D:\DevTools"
$InstallersDir = Join-Path $DevRoot "Installers"
$CachesDir     = Join-Path $DevRoot "Caches"
$TempDir       = Join-Path $DevRoot "Temp"

# Создаём базовые папки
$dirsToCreate = @($DevRoot, $InstallersDir, $CachesDir, $TempDir,
    (Join-Path $CachesDir "pip"),
    (Join-Path $CachesDir "npm"),
    (Join-Path $CachesDir "yarn"),
    (Join-Path $CachesDir "pnpm")
)

foreach ($d in $dirsToCreate) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d | Out-Null
    }
}

# Переназначаем временные переменные для текущей сессии (чтобы меньше засорять C:\Users\...)
$env:TEMP = $TempDir
$env:TMP  = $TempDir

# Настройки кэшей (pip / npm / yarn / pnpm) — на D:\DevTools
[Environment]::SetEnvironmentVariable("PIP_CACHE_DIR", (Join-Path $CachesDir "pip"), "User")

# NPM / YARN / PNPM настроим после установки Node.js

# ---------- ПРОВЕРКА ПРАВ ----------

$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "❌ Скрипт нужно запускать от имени администратора!" -ForegroundColor Red
    Write-Host "Правый клик по PowerShell → 'Запуск от имени администратора'." -ForegroundColor Yellow
    exit 1
}

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-PythonVersion {
    if (Test-Command "python") {
        try {
            $ver = & python --version 2>&1
            return ($ver -replace '[^\d\.]', '')
        } catch {
            return $null
        }
    }
    return $null
}

function Get-NodeVersion {
    if (Test-Command "node") {
        try {
            $ver = & node -v 2>&1
            return ($ver -replace '[^\d\.]', '')
        } catch {
            return $null
        }
    }
    return $null
}

function Test-DockerDesktopInstalled {
    $path = "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
    return (Test-Path $path)
}

function Test-GitInstalled {
    return (Test-Command "git")
}

function Test-WSLEnabled {
    $feature = (dism.exe /online /get-featureinfo /featurename:Microsoft-Windows-Subsystem-Linux | Out-String)
    return ($feature -match "State : Enabled")
}

function Test-VirtualMachinePlatform {
    $feature = (dism.exe /online /get-featureinfo /featurename:VirtualMachinePlatform | Out-String)
    return ($feature -match "State : Enabled")
}

function Test-UbuntuInstalled {
    $dists = (wsl.exe -l -q 2>$null)
    return ($dists -match "Ubuntu")
}

function Test-NvidiaGPU {
    return [bool](Get-WmiObject Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" })
}

function Press-Key {
    Write-Host ""
    Read-Host "Нажми Enter, чтобы продолжить"
}

# ---------- МОДУЛИ УСТАНОВКИ / НАСТРОЙКИ ----------

function Enable-WindowsFeaturesDev {
    Write-Host "`n🧩 Проверка и включение компонентов Windows..." -ForegroundColor Cyan

    if (Test-WSLEnabled) {
        Write-Host "[OK] WSL уже включен." -ForegroundColor Green
    } else {
        Write-Host "[INSTALL] Включаю WSL..." -ForegroundColor Yellow
        dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart | Out-Null
    }

    if (Test-VirtualMachinePlatform) {
        Write-Host "[OK] VirtualMachinePlatform уже включен." -ForegroundColor Green
    } else {
        Write-Host "[INSTALL] Включаю VirtualMachinePlatform..." -ForegroundColor Yellow
        dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart | Out-Null
    }

    Write-Host "[INFO] Пробую включить Hyper-V (если редакция поддерживает)..." -ForegroundColor Yellow
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All -NoRestart -ErrorAction SilentlyContinue | Out-Null

    Write-Host "[OK] Включаю .NET Framework 3.5 (если ещё не включен)..." -ForegroundColor Yellow
    DISM /Online /Enable-Feature /FeatureName:NetFx3 /All /Quiet | Out-Null

    Write-Host "[OK] Включаю поддержку длинных путей..." -ForegroundColor Yellow
    Set-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem -Name LongPathsEnabled -Value 1 -Force

    Write-Host "✔ Базовые Dev-компоненты включены." -ForegroundColor Green
}

function Install-PythonDev {
    Write-Host "`n🐍 Python / pip / Dev-инструменты..." -ForegroundColor Cyan

    $pyVer = Get-PythonVersion
    if ($pyVer) {
        Write-Host "[OK] Python уже установлен: $pyVer" -ForegroundColor Green
        Write-Host "[INFO] Новый глобальный Python не ставлю, чтобы не ломать старые проекты." -ForegroundColor Yellow
    } else {
        Write-Host "[INSTALL] Устанавливаю Python 3.12 (инсталлятор в D:\DevTools\Installers)..." -ForegroundColor Yellow
        $pyUrl = "https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe"
        $pyInstaller = Join-Path $InstallersDir "python-3.12.4-amd64.exe"
        Invoke-WebRequest -Uri $pyUrl -OutFile $pyInstaller
        Start-Process -FilePath $pyInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait
        $pyVer = Get-PythonVersion
        if ($pyVer) {
            Write-Host "[OK] Python установлен: $pyVer" -ForegroundColor Green
        } else {
            Write-Host "[ERR] Python не обнаружен после установки, проверь вручную." -ForegroundColor Red
            return
        }
    }

    Write-Host "[UPDATE] Обновляю pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip

    Write-Host "[INSTALL] pipx (если нет)..." -ForegroundColor Yellow
    python -m pip install pipx
    try { pipx ensurepath } catch {}

    Write-Host "[INSTALL] Базовые Dev-пакеты Python..." -ForegroundColor Yellow
    python -m pip install --upgrade virtualenv poetry jupyterlab ipykernel httpx requests wheel setuptools

    Write-Host "✔ Python Dev окружение готово." -ForegroundColor Green
    Write-Host "[INFO] Для проектов создавай виртуальные окружения на D:, напр.: D:\DevTools\Projects\myproj\venv" -ForegroundColor DarkYellow
}

function Install-NodeDev {
    Write-Host "`n📦 Node.js / npm / yarn / pnpm..." -ForegroundColor Cyan

    $nodeVer = Get-NodeVersion
    if ($nodeVer) {
        Write-Host "[OK] Node.js уже установлен: $nodeVer" -ForegroundColor Green
    } else {
        Write-Host "[INSTALL] Устанавливаю Node.js LTS 18..." -ForegroundColor Yellow
        $nodeUrl = "https://nodejs.org/dist/latest-v18.x/node-v18.20.4-x64.msi"
        $nodeMsi = Join-Path $InstallersDir "node-v18-lts-x64.msi"
        Invoke-WebRequest $nodeUrl -OutFile $nodeMsi
        Start-Process msiexec.exe -Wait -ArgumentList "/I `"$nodeMsi`" /quiet"
        $nodeVer = Get-NodeVersion
        if ($nodeVer) {
            Write-Host "[OK] Node.js установлен: $nodeVer" -ForegroundColor Green
        } else {
            Write-Host "[ERR] Node.js не обнаружен после установки, проверь вручную." -ForegroundColor Red
            return
        }
    }

    Write-Host "[INSTALL] Глобальные инструменты npm..." -ForegroundColor Yellow
    npm install -g yarn pnpm npm-check-updates

    # Настройка кэшей на D:\DevTools\Caches\...
    $npmCache = Join-Path $CachesDir "npm"
    $yarnCache = Join-Path $CachesDir "yarn"
    $pnpmStore = Join-Path $CachesDir "pnpm"

    npm config set cache "$npmCache" --global | Out-Null
    if (Test-Command "yarn") {
        yarn config set cache-folder "$yarnCache" | Out-Null
    }
    if (Test-Command "pnpm") {
        pnpm config set store-dir "$pnpmStore" | Out-Null
    }

    Write-Host "✔ Node.js Dev окружение готово. Кэши перенесены на D:\DevTools\Caches." -ForegroundColor Green
}

function Install-GitDev {
    Write-Host "`n🐙 Git / Git LFS / SSH..." -ForegroundColor Cyan

    if (Test-GitInstalled) {
        $gitVer = (git --version)
        Write-Host "[OK] Git уже установлен: $gitVer" -ForegroundColor Green
    } else {
        Write-Host "[INSTALL] Устанавливаю Git for Windows..." -ForegroundColor Yellow
        $gitUrl = "https://github.com/git-for-windows/git/releases/latest/download/Git-2.47.0-64-bit.exe"
        $gitExe = Join-Path $InstallersDir "Git-2.47.0-64-bit.exe"
        Invoke-WebRequest $gitUrl -OutFile $gitExe
        Start-Process $gitExe -ArgumentList "/VERYSILENT" -Wait
        if (Test-GitInstalled) {
            Write-Host "[OK] Git установлен." -ForegroundColor Green
        } else {
            Write-Host "[ERR] Git не обнаружен после установки, проверь вручную." -ForegroundColor Red
        }
    }

    Write-Host "[INSTALL] Git LFS..." -ForegroundColor Yellow
    git lfs install

    $sshKeyPath = "$env:USERPROFILE\.ssh\id_ed25519"
    if (Test-Path $sshKeyPath) {
        Write-Host "[OK] SSH-ключ уже есть: $sshKeyPath" -ForegroundColor Green
    } else {
        Write-Host "[CREATE] Создаю SSH-ключ ed25519..." -ForegroundColor Yellow
        if (-not (Test-Path "$env:USERPROFILE\.ssh")) {
            New-Item -ItemType Directory -Path "$env:USERPROFILE\.ssh" | Out-Null
        }
        ssh-keygen -t ed25519 -C "dev@local" -f $sshKeyPath -N "" | Out-Null
        Write-Host "[OK] SSH-ключ создан: $sshKeyPath" -ForegroundColor Green
    }

    Write-Host "✔ Git Dev окружение готово." -ForegroundColor Green
}

function Install-DockerDev {
    Write-Host "`n🐳 Docker Desktop..." -ForegroundColor Cyan

    if (Test-DockerDesktopInstalled) {
        Write-Host "[OK] Docker Desktop уже установлен." -ForegroundColor Green
        Write-Host "[INFO] Перенос Docker data-root на D: лучше делать через настройки Docker Desktop вручную." -ForegroundColor DarkYellow
    } else {
        Write-Host "[INSTALL] Устанавливаю Docker Desktop..." -ForegroundColor Yellow
        $dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
        $dockerExe = Join-Path $InstallersDir "DockerDesktopInstaller.exe"
        Invoke-WebRequest $dockerUrl -OutFile $dockerExe
        Start-Process $dockerExe -ArgumentList "install --quiet" -Wait
        if (Test-DockerDesktopInstalled) {
            Write-Host "[OK] Docker Desktop установлен." -ForegroundColor Green
        } else {
            Write-Host "[ERR] Docker Desktop не обнаружен после установки, проверь вручную." -ForegroundColor Red
        }
    }

    Write-Host "[NOTE] Для переноса образов/volume на D: зайди в Docker Desktop → Settings → Resources / Advanced и измени путь disk image." -ForegroundColor Yellow
}

function Install-WSLUbuntu {
    Write-Host "`n🐧 WSL2 + Ubuntu..." -ForegroundColor Cyan

    if (-not (Test-WSLEnabled) -or -not (Test-VirtualMachinePlatform)) {
        Write-Host "[WARN] WSL или VirtualMachinePlatform ещё не включены. Сначала запусти модуль '1 - Базовые компоненты Windows'." -ForegroundColor Yellow
        return
    }

    if (Test-UbuntuInstalled) {
        Write-Host "[OK] Ubuntu уже установлена в WSL." -ForegroundColor Green
        Write-Host "[NOTE] Перенос существующей Ubuntu на D: (через wsl --export / --import) лучше сделать вручную, чтобы не потерять данные." -ForegroundColor Yellow
    } else {
        Write-Host "[INSTALL] Устанавливаю Ubuntu для WSL..." -ForegroundColor Yellow
        try {
            # Стандартная установка; по умолчанию VHDX будет на системном диске,
            # перенос на D: лучше выполнять отдельно через export/import.
            wsl --install -d Ubuntu
            Write-Host "[OK] Ubuntu добавлена. Первичная настройка завершится при первом запуске Ubuntu." -ForegroundColor Green
        } catch {
            Write-Host "[ERR] Не удалось установить Ubuntu автоматически, можно поставить её через Microsoft Store." -ForegroundColor Red
        }
    }
}

function Optimize-NvidiaGPU {
    Write-Host "`n⚡ NVIDIA / CUDA..." -ForegroundColor Cyan

    if (-not (Test-NvidiaGPU)) {
        Write-Host "[INFO] NVIDIA GPU не обнаружена, модуль можно пропустить." -ForegroundColor Yellow
        return
    }

    Write-Host "[OK] NVIDIA GPU обнаружена." -ForegroundColor Green

    Write-Host "[CLEAN] Очищаю стандартный NV_Cache (на C:\)..." -ForegroundColor Yellow
    Remove-Item "C:\ProgramData\NVIDIA Corporation\NV_Cache\*" -Force -Recurse -ErrorAction SilentlyContinue

    Write-Host "[INFO] Сам перенос NV_Cache на D: официально не поддерживается и может ломать драйвера." -ForegroundColor DarkYellow
    Write-Host "[INFO] Рекомендуется просто периодически чистить кэш (как делает этот модуль)." -ForegroundColor DarkYellow
}

function Optimize-WindowsDev {
    Write-Host "`n⚙ Лёгкие твики Windows под разработчика..." -ForegroundColor Cyan

    Write-Host "[TWEAK] Ускорение меню..." -ForegroundColor Yellow
    Set-ItemProperty "HKCU:\Control Panel\Desktop" MenuShowDelay "0" -ErrorAction SilentlyContinue

    Write-Host "[TWEAK] Отключаю рекламу в проводнике..." -ForegroundColor Yellow
    Set-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" ShowSyncProviderNotifications 0 -ErrorAction SilentlyContinue

    Write-Host "[TWEAK] Показ расширений файлов..." -ForegroundColor Yellow
    Set-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced HideFileExt 0 -ErrorAction SilentlyContinue

    Write-Host "[TWEAK] Показ скрытых файлов..." -ForegroundColor Yellow
    Set-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced Hidden 1 -ErrorAction SilentlyContinue

    Write-Host "[INFO] Перезапускаю проводник..." -ForegroundColor Yellow
    Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
    Start-Process explorer.exe

    Write-Host "✔ Основные твики применены." -ForegroundColor Green
}

function Clean-SystemSafe {
    Write-Host "`n🧹 Безопасная очистка системы (включая C:\, но без радикала)..." -ForegroundColor Cyan

    Write-Host "[CLEAN] TEMP-папки Windows и пользователя..." -ForegroundColor Yellow
    $pathsToClean = @(
        "$env:TEMP\*",
        "C:\Windows\Temp\*"
    )
    foreach ($p in $pathsToClean) {
        Remove-Item $p -Recurse -Force -ErrorAction SilentlyContinue
    }

    Write-Host "[CLEAN] Prefetch..." -ForegroundColor Yellow
    Remove-Item "C:\Windows\Prefetch\*" -Recurse -Force -ErrorAction SilentlyContinue

    Write-Host "[CLEAN] Логи CBS/DISM..." -ForegroundColor Yellow
    $logPaths = @(
        "C:\Windows\Logs\CBS\*",
        "C:\Windows\Logs\DISM\*"
    )
    foreach ($log in $logPaths) {
        Remove-Item $log -Force -ErrorAction SilentlyContinue
    }

    Write-Host "[CLEAN] Корзина..." -ForegroundColor Yellow
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue

    Write-Host "[OPT] WinSxS / StartComponentCleanup (безопасный режим)..." -ForegroundColor Yellow
    Dism.exe /online /cleanup-image /startcomponentcleanup | Out-Null

    Write-Host "✔ Очистка завершена." -ForegroundColor Green
}

# ---------- МЕНЮ ----------

function Show-Menu {
    Clear-Host
    Write-Host "===================================" -ForegroundColor DarkGray
    Write-Host "   DEV/AI PRO SMART INSTALLER" -ForegroundColor Cyan
    Write-Host "      D:\DevTools edition" -ForegroundColor Cyan
    Write-Host "===================================" -ForegroundColor DarkGray
    Write-Host "1) Базовые компоненты Windows (WSL, VMPlatform, .NET, LongPaths)" 
    Write-Host "2) Python Dev окружение"
    Write-Host "3) Node.js Dev окружение"
    Write-Host "4) Git + Git LFS + SSH"
    Write-Host "5) Docker Desktop"
    Write-Host "6) WSL2 + Ubuntu"
    Write-Host "7) NVIDIA оптимизация (очистка NV_Cache)"
    Write-Host "8) Твики Windows под разработчика"
    Write-Host "9) Безопасная очистка системы"
    Write-Host "A) ВСЁ ПОДРЯД (1–9)"
    Write-Host "Q) Выход"
    Write-Host "-----------------------------------"
}

do {
    Show-Menu
    $choice = Read-Host "Выбери пункт меню"

    switch ($choice.ToUpper()) {
        "1" { Enable-WindowsFeaturesDev; Press-Key }
        "2" { Install-PythonDev; Press-Key }
        "3" { Install-NodeDev; Press-Key }
        "4" { Install-GitDev; Press-Key }
        "5" { Install-DockerDev; Press-Key }
        "6" { Install-WSLUbuntu; Press-Key }
        "7" { Optimize-NvidiaGPU; Press-Key }
        "8" { Optimize-WindowsDev; Press-Key }
        "9" { Clean-SystemSafe; Press-Key }
        "A" {
            Enable-WindowsFeaturesDev
            Install-PythonDev
            Install-NodeDev
            Install-GitDev
            Install-DockerDev
            Install-WSLUbuntu
            Optimize-NvidiaGPU
            Optimize-WindowsDev
            Clean-SystemSafe
            Press-Key
        }
        "Q" { break }
        default {
            Write-Host "Неверный выбор, попробуй ещё раз." -ForegroundColor Yellow
            Press-Key
        }
    }
} while ($true)

Write-Host "`n🎉 Готово. DEV/AI PRO Smart закончил работу. Рекомендуется перезагрузка." -ForegroundColor Green
