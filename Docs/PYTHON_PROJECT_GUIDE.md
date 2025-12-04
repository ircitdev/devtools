# Создание Python проекта для VS Code + Claude Code

## 🎯 Пошаговая инструкция

### Шаг 1: Создание структуры проекта

#### Вариант A: Автоматически (рекомендуется)

Создам скрипт для автоматического создания проекта...

#### Вариант B: Вручную

```bash
# 1. Создайте папку проекта
cd D:\DevTools\Database
mkdir my-project
cd my-project

# 2. Инициализируйте Git
git init

# 3. Создайте виртуальное окружение
D:\DevTools\Python\venv\Scripts\python.exe -m venv venv

# 4. Активируйте окружение
.\venv\Scripts\activate.ps1

# 5. Обновите pip
python -m pip install --upgrade pip
```

---

## 📁 Правильная структура проекта

### Минимальная структура:

```
my-project/
├── .venv/              # Виртуальное окружение
├── .vscode/            # Настройки VS Code
│   ├── settings.json   # Настройки проекта
│   └── launch.json     # Конфигурация отладки
├── src/                # Исходный код
│   ├── __init__.py
│   └── main.py
├── tests/              # Тесты
│   ├── __init__.py
│   └── test_main.py
├── .gitignore          # Игнорируемые файлы
├── .env.example        # Пример переменных окружения
├── requirements.txt    # Зависимости
└── README.md           # Документация
```

### Полная структура (для больших проектов):

```
my-project/
├── .venv/              # Виртуальное окружение
├── .vscode/            # Настройки VS Code
│   ├── settings.json
│   ├── launch.json
│   └── tasks.json
├── src/                # Исходный код
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── tests/              # Тесты
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py
├── docs/               # Документация
├── scripts/            # Скрипты
├── data/               # Данные
├── .gitignore
├── .env.example
├── .env                # Локальные переменные (не коммитить!)
├── requirements.txt    # Зависимости для production
├── requirements-dev.txt # Зависимости для разработки
├── setup.py            # Установка пакета
├── pyproject.toml      # Конфигурация проекта
└── README.md
```

---

## 🔧 Настройка VS Code

### 1. Создайте `.vscode/settings.json`:

```json
{
  // Python интерпретатор
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",

  // Автоформатирование
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",

  // Линтинг
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,

  // Type checking
  "python.linting.mypyEnabled": true,

  // Тестирование
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,

  // Автоимпорт
  "python.analysis.autoImportCompletions": true,

  // Исключения
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true,
    ".mypy_cache": true
  },

  // Claude Code
  "claude.model": "claude-sonnet-4",
  "claude.contextWindow": 200000
}
```

### 2. Создайте `.vscode/launch.json` (для отладки):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Main",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/src/main.py",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload"
      ],
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Tests",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": [
        "tests",
        "-v"
      ],
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

---

## 📦 Управление зависимостями

### requirements.txt

```txt
# Web Framework
fastapi==0.115.0
uvicorn[standard]==0.32.0

# Database
sqlalchemy==2.0.36
alembic==1.14.0
psycopg2-binary==2.9.10

# HTTP клиент
requests==2.32.3
httpx==0.28.1

# Конфигурация
python-dotenv==1.0.1
pydantic==2.10.5
pydantic-settings==2.7.1

# Работа с данными
pandas==2.3.0
numpy==2.3.0
```

### requirements-dev.txt

```txt
# Включаем production зависимости
-r requirements.txt

# Тестирование
pytest==8.3.4
pytest-cov==6.0.0
pytest-asyncio==0.25.2

# Линтинг и форматирование
black==25.3.0
flake8==7.1.1
mypy==1.14.1
pylint==3.3.3

# Pre-commit hooks
pre-commit==4.0.1

# Дополнительные инструменты
ipython==8.31.0
ipdb==0.13.13
```

### Установка зависимостей:

```bash
# Production
pip install -r requirements.txt

# Development
pip install -r requirements-dev.txt
```

---

## 🗂️ Важные файлы

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Mypy
.mypy_cache/
.dmypy.json

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
```

### .env.example

```env
# Application
APP_NAME=My Project
APP_ENV=development
DEBUG=True

# Database
DATABASE_URL=postgresql://developer:dev_password@localhost:5432/devdb

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Secret
SECRET_KEY=your-secret-key-here
```

### pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=html"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

---

## 🚀 Создание проекта - Полный процесс

### Скрипт автоматического создания

Я создам скрипт, который делает всё автоматически...

### Ручное создание:

```powershell
# 1. Создать структуру
cd D:\DevTools\Database
mkdir my-project
cd my-project

# 2. Создать виртуальное окружение
D:\DevTools\Python\venv\Scripts\python.exe -m venv .venv

# 3. Активировать
.\.venv\Scripts\activate.ps1

# 4. Обновить pip
python -m pip install --upgrade pip

# 5. Создать структуру папок
mkdir src, tests, docs, scripts, data
New-Item -ItemType File src\__init__.py, tests\__init__.py

# 6. Создать main.py
@"
"""Main application module."""

def main():
    print("Hello from My Project!")

if __name__ == "__main__":
    main()
"@ | Out-File -FilePath src\main.py -Encoding UTF8

# 7. Создать requirements
@"
fastapi==0.115.0
uvicorn[standard]==0.32.0
python-dotenv==1.0.1
"@ | Out-File -FilePath requirements.txt -Encoding UTF8

# 8. Создать .gitignore
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# 9. Инициализировать Git
git init
git add .
git commit -m "Initial commit"

# 10. Открыть в VS Code
code .
```

---

## 🎯 Работа с Claude Code

### 1. Откройте проект в VS Code

```powershell
cd D:\DevTools\Database\my-project
code .
```

### 2. Настройте Python интерпретатор

1. Нажмите `Ctrl+Shift+P`
2. Введите: `Python: Select Interpreter`
3. Выберите: `.venv\Scripts\python.exe`

### 3. Используйте Claude Code

**Основные команды:**

```
# Спросить Claude
Ctrl+Shift+P → "Claude: Chat"

# Редактировать код
Выделите код → Ctrl+Shift+P → "Claude: Edit"

# Создать тесты
Откройте файл → Попросите Claude создать тесты

# Рефакторинг
Выделите функцию → Попросите Claude оптимизировать
```

**Примеры запросов к Claude:**

```
"Создай FastAPI приложение с endpoints для CRUD операций"

"Напиши тесты для функции main() с использованием pytest"

"Добавь обработку ошибок и логирование в этот код"

"Создай модель SQLAlchemy для таблицы users"

"Оптимизируй эту функцию для работы с большими данными"
```

### 4. Контекст для Claude

**Claude Code автоматически видит:**
- Открытые файлы
- Структуру проекта
- requirements.txt
- .env файлы
- README.md

**Для лучших результатов:**
- Держите открытыми релевантные файлы
- Создайте хороший README.md
- Комментируйте сложные участки кода

---

## 📝 Пример проекта

### src/main.py

```python
"""Main application module."""
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Загрузить переменные окружения
load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "My Project"),
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### tests/test_main.py

```python
"""Tests for main module."""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

---

## 🔍 Отладка в VS Code

### 1. Установите точку останова (breakpoint)
- Кликните слева от номера строки
- Или нажмите `F9`

### 2. Запустите отладку
- Нажмите `F5`
- Или: Run → Start Debugging

### 3. Используйте Debug Console
- Проверяйте переменные
- Выполняйте код
- Вызывайте функции

### 4. Горячие клавиши отладки:
- `F5` - Continue
- `F10` - Step Over
- `F11` - Step Into
- `Shift+F11` - Step Out
- `Shift+F5` - Stop

---

## 🧪 Тестирование

### Запуск тестов:

```bash
# Все тесты
pytest

# С покрытием кода
pytest --cov=src

# Конкретный файл
pytest tests/test_main.py

# Конкретный тест
pytest tests/test_main.py::test_root

# В режиме watch (при изменениях)
pytest-watch
```

### В VS Code:
1. Откройте панель Testing (иконка колбы)
2. Нажмите "Refresh Tests"
3. Запускайте тесты кликом

---

## 📚 Полезные расширения VS Code

**Обязательные:**
- Python (Microsoft)
- Claude Code (Anthropic)
- Pylance (Microsoft)

**Рекомендуемые:**
- Python Test Explorer
- Better Comments
- GitLens
- Error Lens
- autoDocstring
- Python Indent

---

## 🎓 Best Practices

### 1. Структура кода
```python
"""Module docstring."""
import standard_library
import third_party
import local_modules

# Constants
CONSTANT_VALUE = 100

# Functions
def my_function():
    """Function docstring."""
    pass

# Classes
class MyClass:
    """Class docstring."""
    pass

# Main
if __name__ == "__main__":
    main()
```

### 2. Type hints
```python
def greet(name: str) -> str:
    """Greet a person."""
    return f"Hello, {name}!"
```

### 3. Docstrings
```python
def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b

    Example:
        >>> calculate_sum(2, 3)
        5
    """
    return a + b
```

### 4. Логирование
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Application started")
```

---

## 🚀 Готовый шаблон

Я создам скрипт, который автоматически создает проект со всеми настройками...
