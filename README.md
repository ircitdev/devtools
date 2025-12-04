# DevTools - Complete Windows Development Environment

> 🚀 Полная портативная среда разработки для Windows с Python, Node.js, Docker, и инструментами DevOps

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-22+-green)](https://nodejs.org/)

## 📋 Оглавление

- [О проекте](#о-проекте)
- [Возможности](#возможности)
- [Быстрый старт](#быстрый-старт)
- [Установка](#установка)
- [Документация](#документация)
- [Использование](#использование)
- [Примеры](#примеры)
- [Поддержка](#поддержка)
- [Вклад в проект](#вклад-в-проект)
- [Лицензия](#лицензия)

---

## 🎯 О проекте

**DevTools** - это готовая портативная среда разработки для Windows, которая включает все необходимое для:

- 🐍 **Python разработки** - Data Science, Backend, APIs
- 🌐 **Web разработки** - Node.js, TypeScript, Frontend
- 🐳 **DevOps** - Docker, Terraform, Infrastructure as Code
- 💾 **Работы с базами данных** - PostgreSQL, MySQL, MongoDB, Redis
- 🤖 **AI/ML проектов** - Jupyter, PyTorch, TensorFlow, Anthropic Claude

Всё настроено, интегрировано и готово к использованию!

---

## ✨ Возможности

### 🛠️ Полный набор инструментов

**Языки и среды:**
- ✅ Python 3.11+ с виртуальным окружением
- ✅ Node.js v22+ с TypeScript поддержкой
- ✅ 150+ Python пакетов (FastAPI, pandas, numpy, jupyter, и др.)
- ✅ 9 глобальных npm пакетов (TypeScript, ESLint, Prettier, PM2)

**Базы данных:**
- ✅ Docker Compose для PostgreSQL, MySQL, MongoDB, Redis
- ✅ DBeaver - универсальный клиент БД
- ✅ Готовые подключения и конфигурации

**DevOps инструменты:**
- ✅ Docker + Docker Compose
- ✅ Terraform для Infrastructure as Code
- ✅ Git с готовыми конфигурациями
- ✅ kubectl (через Docker)

**Разработка:**
- ✅ VS Code интеграция
- ✅ Claude Code ready
- ✅ Jupyter Notebook/Lab
- ✅ Postman для API тестирования

**Утилиты:**
- ✅ jq (JSON процессор)
- ✅ tree (визуализация структуры)
- ✅ 7-Zip (архиватор)
- ✅ И многое другое...

### 📦 Автоматизация

- 🔄 **Автоматическое создание проектов** - готовые шаблоны для Python и Node.js
- ⚙️ **Настройка за 1 команду** - весь стек разворачивается автоматически
- 🎯 **Портативность** - всё в одной папке, легко переносить
- 📚 **Полная документация** - руководства по всем компонентам

### 🚀 Скрипты управления

- `DevTools-Manager.ps1` - главный менеджер
- `create-python-project.ps1` - создание Python проектов для VS Code
- `create-node-project.ps1` - создание Node.js проектов
- `backup-devtools.ps1` - резервное копирование
- `update-all.ps1` - обновление всех пакетов

---

## ⚡ Быстрый старт

### Установка за 3 шага:

```powershell
# 1. Клонируйте репозиторий
git clone https://github.com/ircitdev/devtools.git D:\DevTools
cd D:\DevTools

# 2. Запустите установщик (PowerShell от Администратора)
.\install-devtools.ps1

# 3. Настройте компоненты
.\DevTools-Manager.ps1 setup all
```

**Готово!** Через 15 минут у вас полностью рабочая среда разработки.

---

## 📥 Установка

### Системные требования:

- **ОС:** Windows 10/11 (64-bit)
- **RAM:** 8 GB (рекомендуется 16 GB)
- **Диск:** 10 GB свободного места
- **Обязательное ПО:** Python 3.11+, Node.js 18+, Git

### Предварительные требования:

1. **Python 3.11+** - [Скачать](https://www.python.org/downloads/)
2. **Node.js 18+** - [Скачать](https://nodejs.org/)
3. **Git** - [Скачать](https://git-scm.com/download/win)
4. **Docker Desktop** (опционально) - [Скачать](https://www.docker.com/products/docker-desktop)

### Подробная установка:

См. [INSTALL.md](INSTALL.md) для детальных инструкций.

---

## 📚 Документация

### Основная документация:

- **[INSTALL.md](INSTALL.md)** - Подробная инструкция установки
- **[QUICKSTART.md](QUICKSTART.md)** - Быстрый старт
- **[PYTHON_PROJECT_QUICKSTART.md](PYTHON_PROJECT_QUICKSTART.md)** - Создание Python проектов

### Руководства (в папке Docs/):

- **[PYTHON_PROJECT_GUIDE.md](Docs/PYTHON_PROJECT_GUIDE.md)** - Полное руководство по Python проектам
- **[PYTHON_GUIDE.md](Docs/PYTHON_GUIDE.md)** - Работа с Python
- **[NODEJS_GUIDE.md](Docs/NODEJS_GUIDE.md)** - Работа с Node.js
- **[DOCKER_GUIDE.md](Docs/DOCKER_GUIDE.md)** - Работа с Docker
- **[JUPYTER_GUIDE.md](Docs/JUPYTER_GUIDE.md)** - Jupyter Notebook
- **[GITHUB_GUIDE.md](Docs/GITHUB_GUIDE.md)** - GitHub интеграция
- **[STRUCTURE.md](Docs/STRUCTURE.md)** - Структура проекта

---

## 🎯 Использование

### Создание Python проекта:

```powershell
# FastAPI проект
.\Scripts\create-python-project.ps1 my-api -Template fastapi

# Data Science проект
.\Scripts\create-python-project.ps1 analysis -Template data-science

# CLI приложение
.\Scripts\create-python-project.ps1 tool -Template cli
```

### Создание Node.js проекта:

```powershell
# TypeScript проект
.\Scripts\create-node-project.ps1 my-app -Template typescript

# Express API
.\Scripts\create-node-project.ps1 my-api -Template express
```

### Управление Docker:

```powershell
# Запустить базы данных
.\DevTools-Manager.ps1 docker start

# Остановить
.\DevTools-Manager.ps1 docker stop

# Статус
.\DevTools-Manager.ps1 docker status
```

### Запуск Jupyter:

```powershell
.\Scripts\start-jupyter.ps1
# или
.\Scripts\start-jupyterlab.ps1
```

---

## 💡 Примеры

### Пример 1: FastAPI CRUD API

```powershell
# Создать проект
.\Scripts\create-python-project.ps1 users-api -Template fastapi
cd Database\users-api

# Открыть в VS Code
code .

# Попросить Claude Code создать CRUD API
# F5 для запуска
# Открыть http://localhost:8000/docs
```

### Пример 2: Data Analysis с Jupyter

```powershell
# Создать проект
.\Scripts\create-python-project.ps1 sales-analysis -Template data-science

# Запустить Jupyter
.\Scripts\start-jupyter.ps1

# Открыть example_notebook.ipynb
```

### Пример 3: TypeScript + Express

```powershell
# Создать проект
.\Scripts\create-node-project.ps1 api -Template express

# Перейти в проект
cd Database\api

# Установить зависимости
npm install

# Запустить
npm run dev
```

---

## 🗂️ Структура проекта

```
DevTools/
├── install-devtools.ps1       # Главный установщик
├── DevTools-Manager.ps1       # Менеджер управления
│
├── Python/                    # Python окружение
│   ├── venv/                  # Виртуальное окружение
│   ├── setup_python.ps1       # Установка Python
│   └── activate.ps1           # Активация venv
│
├── NodeJS/                    # Node.js окружение
│   ├── global_modules/        # Глобальные пакеты
│   └── setup_nodejs.ps1       # Установка Node.js
│
├── Docker/                    # Docker конфигурация
│   ├── compose/               # Compose файлы
│   └── setup_docker.ps1       # Установка Docker
│
├── Scripts/                   # Утилиты
│   ├── create-python-project.ps1
│   ├── create-node-project.ps1
│   ├── backup-devtools.ps1
│   └── update-all.ps1
│
└── Docs/                      # Документация
    ├── PYTHON_GUIDE.md
    ├── NODEJS_GUIDE.md
    └── ...
```

---

## 🤝 Поддержка

### Возникли проблемы?

1. Проверьте [INSTALL.md](INSTALL.md) - раздел "Решение проблем"
2. Посмотрите [Issues](https://github.com/ircitdev/devtools/issues)
3. Создайте новый Issue

### Вопросы?

- 📖 Читайте документацию в `Docs/`
- 💬 Создайте Discussion
- 🐛 Создайте Issue для багов

---

## 🌟 Вклад в проект

Contributions are welcome!

1. Fork репозиторий
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

---

## 📜 Лицензия

Распространяется под лицензией MIT. См. `LICENSE` для подробностей.

---

## 🙏 Благодарности

- [Python Software Foundation](https://www.python.org/)
- [Node.js Foundation](https://nodejs.org/)
- [Docker Inc.](https://www.docker.com/)
- [Chocolatey Software](https://chocolatey.org/)
- [Anthropic](https://www.anthropic.com/) (Claude Code)
- Всем разработчикам open-source пакетов

---

## 📊 Статистика

- **150+** Python пакетов
- **9** Node.js глобальных пакетов
- **20+** готовых скриптов
- **10+** документаций
- **4** Docker Compose шаблона
- **5** шаблонов проектов

---

## 🎯 Roadmap

- [ ] Добавить поддержку Go
- [ ] Добавить поддержку Rust
- [ ] Kubernetes интеграция (Minikube)
- [ ] CI/CD шаблоны (GitHub Actions)
- [ ] Больше проектных шаблонов
- [ ] GUI установщик

---

## 📞 Контакты

- **GitHub:** [@ircitdev](https://github.com/ircitdev)
- **Repository:** [devtools](https://github.com/ircitdev/devtools)

---

<div align="center">

**Сделано с ❤️ для разработчиков**

⭐ Поставьте звезду, если проект полезен!

[Установка](#установка) • [Документация](#документация) • [Примеры](#примеры)

</div>
