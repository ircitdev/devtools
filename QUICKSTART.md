# DevTools - Быстрый старт

> ⚡ Начните использовать DevTools за 5 минут

## 🚀 Установка

### 1. Клонируйте репозиторий

```powershell
git clone https://github.com/ircitdev/devtools.git D:\DevTools
cd D:\DevTools
```

### 2. Запустите установщик

```powershell
# PowerShell от Администратора
.\install-devtools.ps1
```

**Что будет установлено:**
- Python 3.11+ virtual environment с 150+ пакетами
- Node.js v22+ с TypeScript, ESLint, Prettier, PM2
- Docker Compose для баз данных (PostgreSQL, MySQL, MongoDB, Redis)
- DBeaver (клиент БД), Postman (API тестирование)
- Terraform, jq, tree, 7-Zip

**Время установки:** ~15-20 минут

### 3. Проверьте установку

```powershell
.\DevTools-Manager.ps1 status
```

---

## 📦 Создание проектов

### Python проект

```powershell
# FastAPI проект
.\Scripts\create-python-project.ps1 my-api -Template fastapi

# Data Science проект
.\Scripts\create-python-project.ps1 analysis -Template data-science

# CLI приложение
.\Scripts\create-python-project.ps1 tool -Template cli
```

### Node.js проект

```powershell
# TypeScript проект
.\Scripts\create-node-project.ps1 my-app -Template typescript

# Express API
.\Scripts\create-node-project.ps1 my-api -Template express
```

---

## 🎯 Основные команды

### DevTools Manager

```powershell
# Проверить статус
.\DevTools-Manager.ps1 status

# Docker команды
.\DevTools-Manager.ps1 docker start
.\DevTools-Manager.ps1 docker stop
```

### Python

```powershell
# Активировать venv
.\Python\activate.ps1

# Jupyter Notebook
.\Scripts\start-jupyter.ps1
```

### Node.js

```powershell
# Активировать окружение
.\Scripts\node-env.ps1
```

**Готово! Начинайте разработку! 🚀**
