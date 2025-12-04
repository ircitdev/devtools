# GitHub Workflow - Правильная работа с GitHub в новых проектах

> Полное руководство по работе с GitHub для DevTools проектов

## 📋 Содержание

- [Создание нового проекта](#создание-нового-проекта)
- [Клонирование существующих репозиториев](#клонирование-существующих-репозиториев)
- [Ежедневный Git workflow](#ежедневный-git-workflow)
- [Работа с ветками](#работа-с-ветками)
- [Commit messages](#commit-messages)
- [Работа с .gitignore](#работа-с-gitignore)
- [Работа с секретами](#работа-с-секретами)
- [Best practices](#best-practices)
- [Типичные проблемы](#типичные-проблемы)
- [Полезные команды](#полезные-команды)

---

## 🚀 Создание нового проекта

### Способ 1: Создать проект локально, затем загрузить на GitHub (рекомендуется)

```powershell
# 1. Создайте Python проект с помощью DevTools
.\Scripts\create-python-project.ps1 my-new-project -Template fastapi
cd Database\my-new-project

# 2. Инициализируйте Git
git init

# 3. Добавьте все файлы
git add .

# 4. Первый коммит
git commit -m "Initial commit: FastAPI project setup"

# 5. Создайте репозиторий на GitHub (через веб-интерфейс или CLI)
# Веб: https://github.com/new
# Или используйте GitHub CLI:
gh repo create my-new-project --public --source=. --remote=origin --push
```

### Способ 2: Использовать GitHub CLI (gh)

```powershell
# 1. Создайте проект
.\Scripts\create-python-project.ps1 my-api -Template fastapi
cd Database\my-api

# 2. Инициализируйте git и создайте репозиторий одной командой
git init
git add .
git commit -m "Initial commit"
gh repo create my-api --public --source=. --push
```

### Способ 3: Клонировать пустой репозиторий с GitHub

```powershell
# 1. Создайте пустой репозиторий на GitHub (через веб-интерфейс)

# 2. Клонируйте его
cd D:\DevTools\Database
git clone https://github.com/ircitdev/my-new-project.git
cd my-new-project

# 3. Добавьте код
# Скопируйте шаблон или напишите код

# 4. Коммит и push
git add .
git commit -m "Initial commit"
git push origin main
```

---

## 📥 Клонирование существующих репозиториев

### Вариант 1: Публичный репозиторий

```powershell
cd D:\DevTools\Database
git clone https://github.com/username/repo-name.git
cd repo-name
```

### Вариант 2: Приватный репозиторий (с аутентификацией)

```powershell
# Используйте скрипт с автоматической аутентификацией
.\Scripts\git-clone-auth.ps1 username/repo-name

# Или вручную с токеном из .env
$token = (Get-Content "Config\.env" | Select-String "GITHUB_TOKEN").ToString().Split("=")[1]
git clone https://ircitdev:$token@github.com/ircitdev/private-repo.git
```

### Вариант 3: С помощью GitHub CLI

```powershell
gh repo clone username/repo-name
```

---

## 📝 Ежедневный Git workflow

### Базовый цикл разработки

```powershell
# 1. Проверить текущее состояние
git status

# 2. Посмотреть изменения
git diff

# 3. Добавить файлы в staging
git add filename.py
# Или все файлы:
git add .

# 4. Коммит
git commit -m "feat: add user authentication"

# 5. Push на GitHub
git push origin main
```

### Детальный workflow

```powershell
# Начало рабочего дня
# =====================

# 1. Получить последние изменения
git pull origin main

# Работа над кодом
# =====================

# 2. Проверить что изменилось
git status
# Увидите:
# modified:   src/main.py
# modified:   tests/test_main.py

# 3. Посмотреть детали изменений
git diff src/main.py

# 4. Добавить изменения поэтапно
git add src/main.py
git add tests/test_main.py

# Или все сразу:
git add .

# 5. Проверить что в staging
git status
# Увидите файлы в "Changes to be committed"

# Коммит и отправка
# =====================

# 6. Создать коммит с хорошим сообщением
git commit -m "feat: add user login endpoint

- Implemented POST /api/auth/login
- Added JWT token generation
- Created login tests
- Updated API documentation"

# 7. Отправить на GitHub
git push origin main

# Конец рабочего дня
# =====================

# 8. Убедиться что все закоммичено
git status
# Должно быть: "nothing to commit, working tree clean"
```

---

## 🌿 Работа с ветками

### Зачем нужны ветки?

- **main/master** - стабильная версия, всегда рабочая
- **feature/feature-name** - разработка новых функций
- **fix/bug-name** - исправление багов
- **refactor/component** - рефакторинг кода

### Создание и работа с ветками

```powershell
# Создать новую ветку и переключиться на неё
git checkout -b feature/user-authentication

# Или в два шага:
git branch feature/user-authentication
git checkout feature/user-authentication

# Посмотреть все ветки
git branch
# * feature/user-authentication  (текущая)
#   main

# Работать как обычно
git add .
git commit -m "feat: implement login"

# Отправить ветку на GitHub
git push origin feature/user-authentication

# Вернуться на main
git checkout main

# Удалить локальную ветку (после merge)
git branch -d feature/user-authentication
```

### Feature Branch Workflow (рекомендуется)

```powershell
# 1. Начать новую фичу
git checkout main
git pull origin main
git checkout -b feature/add-dashboard

# 2. Разработка
# ... делаете изменения ...
git add .
git commit -m "feat: add dashboard component"

# 3. Push фичи на GitHub
git push origin feature/add-dashboard

# 4. Создать Pull Request на GitHub
gh pr create --title "Add dashboard" --body "Implements user dashboard with analytics"

# 5. После code review и approval - merge через GitHub UI

# 6. Обновить локальный main
git checkout main
git pull origin main

# 7. Удалить локальную ветку
git branch -d feature/add-dashboard
```

---

## 💬 Commit messages

### Формат Conventional Commits (рекомендуется)

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Типы (type):

- **feat:** - новая функция
- **fix:** - исправление бага
- **docs:** - изменения в документации
- **style:** - форматирование, отсутствие изменений в коде
- **refactor:** - рефакторинг кода
- **test:** - добавление/изменение тестов
- **chore:** - обновление зависимостей, конфигурации

### Примеры хороших commit messages

```powershell
# Простой коммит
git commit -m "feat: add user registration"

# С деталями
git commit -m "feat(auth): add user registration

- Implemented POST /api/auth/register endpoint
- Added email validation
- Created user model and database migration
- Added registration tests"

# Исправление бага
git commit -m "fix(api): correct validation in login endpoint

Fixed issue where empty passwords were accepted.
Closes #42"

# Документация
git commit -m "docs: update API documentation for v2.0"

# Рефакторинг
git commit -m "refactor(database): optimize user queries

Replaced N+1 queries with single join query.
Performance improvement: 200ms -> 20ms"
```

### Примеры плохих commit messages (избегайте)

```powershell
# ❌ Слишком общее
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"

# ❌ Без контекста
git commit -m "oops"
git commit -m "try again"
git commit -m "final version"

# ❌ Множественные изменения без описания
git commit -m "add feature and fix bugs and update docs"
```

---

## 📄 Работа с .gitignore

### Что должно быть в .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/
*.egg-info/
dist/
build/

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# Секреты и credentials
.env
.env.local
*.key
*.pem
credentials.json
config/secrets.yaml

# Базы данных
*.sqlite
*.db
*.sql

# Логи
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Кэши
.cache/
.pytest_cache/
.mypy_cache/
node_modules/

# Временные файлы
*.tmp
*.temp
*.bak
```

### Проверка .gitignore

```powershell
# Показать что будет игнорироваться
git status --ignored

# Проверить будет ли файл игнорироваться
git check-ignore -v .env
# Вывод: .gitignore:5:.env    .env

# Удалить из Git файл, который уже был закоммичен
git rm --cached .env
git commit -m "chore: remove .env from git"
```

### Глобальный .gitignore (опционально)

```powershell
# Создать глобальный .gitignore для всех проектов
$global_gitignore = "$env:USERPROFILE\.gitignore_global"

@"
# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Temporary
*.tmp
*.bak
"@ | Set-Content $global_gitignore

# Настроить Git использовать его
git config --global core.excludesfile $global_gitignore
```

---

## 🔐 Работа с секретами

### Никогда не коммитьте:

- Пароли
- API ключи
- Токены доступа
- Приватные ключи
- Database credentials
- Файлы .env с реальными данными

### Правильный подход

```powershell
# 1. Создайте .env.example с шаблоном
@"
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys
ANTHROPIC_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here

# GitHub
GITHUB_TOKEN=your_github_token_here
"@ | Set-Content .env.example

# 2. Добавьте .env.example в Git
git add .env.example
git commit -m "docs: add environment variables template"

# 3. Создайте реальный .env (он в .gitignore)
Copy-Item .env.example .env
# Отредактируйте .env с реальными данными

# 4. .env НЕ будет закоммичен благодаря .gitignore
git status
# .env не появится в списке
```

### Если случайно закоммитили секрет

```powershell
# ⚠️ ВАЖНО: Если секрет уже был отправлен на GitHub:
# 1. НЕМЕДЛЕННО смените пароль/токен/ключ
# 2. Затем удалите из Git:

# Удалить файл из последнего коммита
git rm --cached .env
git commit --amend -m "chore: remove sensitive file"

# Если файл был в нескольких коммитах - используйте git filter-branch
# или BFG Repo-Cleaner (https://rtyley.github.io/bfg-repo-cleaner/)

# Force push (ОСТОРОЖНО!)
git push --force origin main
```

---

## ✅ Best practices

### 1. Коммитьте часто

```powershell
# ✅ Хорошо: маленькие, частые коммиты
git commit -m "feat: add user model"
git commit -m "feat: add user validation"
git commit -m "test: add user model tests"

# ❌ Плохо: один большой коммит в конце дня
git commit -m "add entire user system"
```

### 2. Делайте pull перед началом работы

```powershell
# Каждый день перед началом
git checkout main
git pull origin main

# Перед созданием feature branch
git checkout main
git pull origin main
git checkout -b feature/new-feature
```

### 3. Проверяйте git status перед коммитом

```powershell
# Всегда проверяйте что коммитите
git status
git diff

# Потом коммит
git add .
git commit -m "feat: add feature"
```

### 4. Пишите описательные commit messages

```powershell
# ✅ Хорошо
git commit -m "fix(auth): prevent null pointer in token validation

Added null check before accessing token.claims.
Fixes issue where expired tokens caused server crash."

# ❌ Плохо
git commit -m "fix"
```

### 5. Используйте ветки для новых фич

```powershell
# ✅ Хорошо
git checkout -b feature/user-dashboard
# ... работа ...
git push origin feature/user-dashboard
# Create Pull Request

# ❌ Плохо - работа напрямую в main
git checkout main
# ... работа ...
git push origin main
```

### 6. Code Review через Pull Requests

```powershell
# 1. Создать feature branch
git checkout -b feature/new-api

# 2. Разработка и коммиты
git commit -m "feat: implement new API"

# 3. Push
git push origin feature/new-api

# 4. Создать PR
gh pr create --title "New API implementation" \
  --body "## Changes
- Added new REST API endpoints
- Implemented authentication
- Added comprehensive tests

## Testing
Tested locally with pytest. All tests pass."

# 5. Дождаться review и approval
# 6. Merge через GitHub UI
```

### 7. Синхронизируйте с upstream

```powershell
# Если работаете с fork репозитория
git remote add upstream https://github.com/original/repo.git

# Регулярно синхронизируйте
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## 🚨 Типичные проблемы

### Проблема 1: Merge конфликты

```powershell
# При pull возник конфликт
git pull origin main
# CONFLICT (content): Merge conflict in src/main.py

# Решение:
# 1. Откройте файл с конфликтом в VS Code
# VS Code покажет конфликты с кнопками "Accept Current" / "Accept Incoming"

# 2. Или вручную отредактируйте:
# <<<<<<< HEAD
# ваши изменения
# =======
# изменения с сервера
# >>>>>>> branch-name

# 3. После разрешения конфликтов
git add src/main.py
git commit -m "merge: resolve conflicts in main.py"
git push origin main
```

### Проблема 2: Нужно отменить последний коммит

```powershell
# Отменить последний коммит, но сохранить изменения
git reset --soft HEAD~1

# Отменить последний коммит и изменения
git reset --hard HEAD~1

# Если уже сделали push (ОСТОРОЖНО!)
git reset --hard HEAD~1
git push --force origin main  # ⚠️ Опасно для shared branches!
```

### Проблема 3: Забыли переключиться на feature branch

```powershell
# Сделали изменения в main, но хотели в feature branch

# Если ещё не закоммитили:
git stash
git checkout -b feature/my-feature
git stash pop

# Если уже закоммитили:
git checkout -b feature/my-feature  # создаёт branch с текущим HEAD
git checkout main
git reset --hard origin/main  # сбрасывает main на серверную версию
```

### Проблема 4: Случайно добавили файл

```powershell
# Удалить из staging (до коммита)
git reset HEAD filename.py

# Удалить из последнего коммита
git rm --cached filename.py
git commit --amend --no-edit

# Полностью откатить изменения в файле
git checkout -- filename.py
```

### Проблема 5: .gitignore не работает

```powershell
# Файл уже был добавлен в git до добавления в .gitignore

# Решение: удалить из git (но оставить локально)
git rm --cached filename
git rm -r --cached directory/

# Коммит
git commit -m "chore: remove ignored files from git"

# Теперь .gitignore будет работать
```

### Проблема 6: Push rejected (non-fast-forward)

```powershell
# Ошибка при push
git push origin main
# error: failed to push some refs

# Решение 1: Pull и merge
git pull origin main
# Разрешите конфликты если есть
git push origin main

# Решение 2: Rebase (если вы один работаете)
git pull --rebase origin main
git push origin main

# Решение 3: Force push (⚠️ ОПАСНО - только если вы один!)
git push --force origin main
```

---

## 📚 Полезные команды

### Просмотр истории

```powershell
# История коммитов
git log

# Компактный вид
git log --oneline

# С графом веток
git log --oneline --graph --all

# Последние 5 коммитов
git log -5

# История конкретного файла
git log --follow filename.py

# Кто и что менял в файле
git blame filename.py
```

### Информация о коммитах

```powershell
# Детали конкретного коммита
git show abc123

# Изменения в коммите
git show abc123 --stat

# Список файлов в коммите
git diff-tree --no-commit-id --name-only -r abc123
```

### Работа с удалёнными репозиториями

```powershell
# Список удалённых репозиториев
git remote -v

# Добавить удалённый репозиторий
git remote add upstream https://github.com/original/repo.git

# Изменить URL
git remote set-url origin https://new-url.git

# Удалить удалённый репозиторий
git remote remove upstream

# Информация о remote
git remote show origin
```

### Поиск

```powershell
# Поиск в коде
git grep "search_term"

# Поиск в истории
git log --all --grep="bug fix"

# Найти когда была добавлена строка
git log -S "specific_code_line" --source --all
```

### Stash (временное сохранение)

```powershell
# Сохранить изменения временно
git stash

# С сообщением
git stash save "WIP: working on feature"

# Список stash
git stash list

# Применить последний stash
git stash pop

# Применить конкретный stash
git stash apply stash@{0}

# Удалить stash
git stash drop stash@{0}

# Очистить все stash
git stash clear
```

### Откат изменений

```powershell
# Откатить изменения в файле
git checkout -- filename.py

# Откатить все изменения
git checkout -- .

# Откатить к конкретному коммиту
git reset --hard abc123

# Создать коммит который отменяет изменения
git revert abc123
```

---

## 🎯 Workflow для DevTools проектов

### Создание нового Python проекта

```powershell
# 1. Создать проект
cd D:\DevTools
.\Scripts\create-python-project.ps1 my-api -Template fastapi

# 2. Перейти в проект
cd Database\my-api

# 3. Инициализировать Git
git init

# 4. Добавить .gitignore (уже создан скриптом)
git add .gitignore

# 5. Первый коммит
git add .
git commit -m "chore: initial FastAPI project setup

Created with DevTools create-python-project.ps1
Template: fastapi

Project structure:
- src/ - source code
- tests/ - pytest tests
- .vscode/ - VS Code configuration
- requirements.txt - Python dependencies"

# 6. Создать репозиторий на GitHub
gh repo create my-api --public --source=. --push

# 7. Начать разработку
code .
```

### Ежедневная работа с проектом

```powershell
# Утро - начало работы
cd Database\my-api
git pull origin main

# Создать feature branch
git checkout -b feature/add-users-endpoint

# Разработка в VS Code с Claude Code
# ... пишете код ...

# Проверить изменения
git status
git diff

# Коммит
git add .
git commit -m "feat(api): add users CRUD endpoints

- Implemented GET /users
- Implemented POST /users
- Implemented PUT /users/{id}
- Implemented DELETE /users/{id}
- Added Pydantic models
- Added tests for all endpoints"

# Push feature branch
git push origin feature/add-users-endpoint

# Создать Pull Request
gh pr create --title "Add users CRUD endpoints" \
  --body "Implements user management API endpoints with full CRUD operations."

# После merge PR - обновить main
git checkout main
git pull origin main
git branch -d feature/add-users-endpoint
```

---

## 🔗 Полезные ссылки

### Документация:
- **Git Documentation:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com/
- **GitHub CLI:** https://cli.github.com/
- **Conventional Commits:** https://www.conventionalcommits.org/

### Интерактивное обучение:
- **Learn Git Branching:** https://learngitbranching.js.org/
- **GitHub Skills:** https://skills.github.com/
- **Git Immersion:** https://gitimmersion.com/

### Инструменты:
- **GitLens (VS Code):** См. [GITLENS_GUIDE.md](GITLENS_GUIDE.md)
- **GitHub Desktop:** https://desktop.github.com/
- **Git GUI Tools:** GitKraken, SourceTree, Fork

---

## 📝 Cheat Sheet

### Базовые команды

```powershell
# Инициализация
git init                          # Создать репозиторий
git clone <url>                   # Клонировать репозиторий

# Статус и изменения
git status                        # Текущее состояние
git diff                          # Изменения
git diff --staged                 # Изменения в staging

# Добавление и коммит
git add <file>                    # Добавить файл
git add .                         # Добавить все
git commit -m "message"           # Коммит
git commit --amend                # Изменить последний коммит

# Ветки
git branch                        # Список веток
git branch <name>                 # Создать ветку
git checkout <branch>             # Переключиться
git checkout -b <branch>          # Создать и переключиться
git merge <branch>                # Слить ветку
git branch -d <branch>            # Удалить ветку

# Удалённые репозитории
git remote -v                     # Список remote
git fetch                         # Получить изменения
git pull                          # Fetch + merge
git push origin <branch>          # Отправить изменения

# История
git log                           # История коммитов
git log --oneline --graph         # Компактный вид
git show <commit>                 # Детали коммита

# Откат
git reset --soft HEAD~1           # Отменить коммит
git reset --hard HEAD~1           # Отменить коммит и изменения
git checkout -- <file>            # Откатить файл
git revert <commit>               # Создать откат-коммит
```

---

## 💡 Советы для новичков

1. **Коммитьте часто** - лучше много маленьких коммитов, чем один большой
2. **Pull перед push** - всегда делайте `git pull` перед `git push`
3. **Проверяйте status** - `git status` перед каждым коммитом
4. **Пишите понятные messages** - вы поблагодарите себя через месяц
5. **Используйте branches** - не бойтесь создавать ветки
6. **Не коммитьте секреты** - проверьте .gitignore
7. **Используйте GitLens** - визуализация помогает понять Git
8. **Практикуйтесь** - создайте тестовый репозиторий и экспериментируйте

---

**Сделано для DevTools Environment**

Это руководство является частью проекта DevTools и оптимизировано для workflow с Python, Node.js, Docker и Claude Code.

См. также:
- [GITHUB_GUIDE.md](GITHUB_GUIDE.md) - Интеграция с GitHub
- [GITLENS_GUIDE.md](GITLENS_GUIDE.md) - GitLens для VS Code
- [PYTHON_PROJECT_GUIDE.md](PYTHON_PROJECT_GUIDE.md) - Создание Python проектов
