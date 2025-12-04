# GitHub Integration Guide

## ✅ Ваши credentials сохранены

Ваши GitHub credentials безопасно сохранены в:
- `D:\DevTools\Config\.env`
- `D:\DevTools\Config\.github-credentials`

**ВАЖНО:** Эти файлы добавлены в `.gitignore` и НЕ будут коммититься в Git!

## 🔑 Настройка

### Git уже настроен:
```
User: ircitdev
Email: ircitdev@users.noreply.github.com
```

## 📦 Клонирование репозиториев

### Способ 1: С помощью скрипта (рекомендуется)

```powershell
# Клонировать репозиторий
.\Scripts\git-clone-auth.ps1 repository-name

# Клонировать в конкретную папку
.\Scripts\git-clone-auth.ps1 repository-name "D:\Projects\my-project"
```

### Способ 2: Вручную с токеном

```bash
git clone https://ircitdev:YOUR_TOKEN@github.com/ircitdev/repo-name.git
```

### Способ 3: С помощью GitHub CLI

```powershell
# Настроить gh CLI
# Ваш токен хранится в Config/.env
$token = Get-Content "Config\.env" | Select-String "GITHUB_TOKEN" | ForEach-Object { $_.ToString().Split('=')[1] }
echo $token | gh auth login --with-token

# Клонировать репозиторий
gh repo clone ircitdev/repo-name
```

## 🔐 Использование токена

Ваш GitHub Personal Access Token хранится в `Config/.env`

Чтобы получить токен:
```powershell
# PowerShell
Get-Content "Config\.env" | Select-String "GITHUB_TOKEN"
```

### Для HTTPS клонирования:
```bash
# Используйте YOUR_TOKEN из Config/.env
git clone https://ircitdev:YOUR_TOKEN@github.com/ircitdev/repo.git
```

### Для существующих репозиториев:
```bash
# Изменить remote URL
git remote set-url origin https://ircitdev:TOKEN@github.com/ircitdev/repo.git

# Проверить
git remote -v
```

## 🔄 Базовые Git операции

### Создать новый репозиторий
```bash
mkdir my-project
cd my-project
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://ircitdev:TOKEN@github.com/ircitdev/my-project.git
git push -u origin main
```

### Обновить существующий репозиторий
```bash
git add .
git commit -m "Update files"
git push
```

### Получить изменения
```bash
git pull
```

## 🛡️ Безопасность

### ✅ Безопасно:
- Токен хранится в `.env` файле (в `.gitignore`)
- Токен НЕ будет виден в истории Git
- Файлы с credentials защищены

### ⚠️ Важно:
- **НИКОГДА** не коммитьте `.env` файл
- **НИКОГДА** не коммитьте `.github-credentials`
- Используйте скрипты для клонирования

### Проверка .gitignore:
```bash
# Убедитесь, что .env в игноре
git check-ignore -v Config/.env
```

## 🔧 Настройка credential helper

Чтобы Git сохранял credentials:
```bash
# Включить credential helper
git config --global credential.helper store

# Первый раз введите credentials вручную, они сохранятся
git clone https://github.com/ircitdev/repo.git
# Username: ircitdev
# Password: [вставьте токен]
```

## 📝 Быстрые команды

### Создать .gitignore для проекта
```bash
cp D:\DevTools\Git\config\.gitignore .gitignore
```

### Проверить статус
```bash
git status
```

### Посмотреть коммиты
```bash
git log --oneline -10
```

### Создать ветку
```bash
git checkout -b feature-name
```

### Переключиться на ветку
```bash
git checkout main
```

## 🆘 Решение проблем

### "Authentication failed"
1. Проверьте токен в `.env` файле
2. Убедитесь, что токен не истек
3. Используйте скрипт `git-clone-auth.ps1`

### "Permission denied"
1. Проверьте, что токен имеет нужные права (repo, workflow)
2. Проверьте username: должен быть `ircitdev`

### Сбросить credentials
```bash
# Windows
cmdkey /delete:git:https://github.com

# Или удалить файл
rm ~/.git-credentials
```

## 📚 Полезные ссылки

- GitHub Docs: https://docs.github.com/
- Git Documentation: https://git-scm.com/doc
- GitHub CLI: https://cli.github.com/

## 🎯 Примеры использования

### Пример 1: Клонировать приватный репозиторий
```powershell
.\Scripts\git-clone-auth.ps1 my-private-repo
cd my-private-repo
```

### Пример 2: Создать и запушить новый проект
```bash
cd D:\Projects
mkdir my-new-project
cd my-new-project

# Инициализировать Git
git init

# Создать файлы
echo "# My Project" > README.md

# Коммит
git add .
git commit -m "Initial commit"

# Создать репозиторий на GitHub через CLI
gh repo create my-new-project --private --source=. --remote=origin --push
```

### Пример 3: Работа с существующим репозиторием
```bash
# Клонировать
.\Scripts\git-clone-auth.ps1 existing-repo

# Изменить файлы
cd existing-repo
# ... редактировать файлы ...

# Закоммитить и запушить
git add .
git commit -m "Update documentation"
git push
```

---

**Ваш GitHub account:** ircitdev
**Token expires:** Проверьте в GitHub Settings > Developer settings > Personal access tokens

**Все готово для работы с GitHub!** 🚀
