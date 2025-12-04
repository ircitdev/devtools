# DevTools - Структура проекта

## Обзор

D:\DevTools - портативная среда разработки, организованная для максимального удобства и переносимости.

## Полная структура директорий

```
D:\DevTools\
│
├── 📁 AI/                          # AI инструменты и модели
│   ├── env/                        # Python venv для AI (torch, tensorflow, whisper)
│   ├── scripts/                    # AI скрипты
│   ├── logs/                       # Логи AI операций
│   ├── temp/                       # Временные файлы
│   ├── install_voice_deps.ps1      # Установка зависимостей голосовых инструментов
│   ├── run_whisper.ps1             # Запуск Whisper
│   └── run_whisper_batch.ps1       # Пакетная обработка Whisper
│
├── 📁 Python/                      # Python окружение
│   ├── venv/                       # Виртуальное окружение
│   │   ├── Scripts/                # Исполняемые файлы (python.exe, pip.exe)
│   │   └── Lib/                    # Библиотеки
│   ├── portable/                   # Портативная копия Python
│   ├── setup_python.ps1            # Установка Python окружения
│   ├── activate.ps1                # Активация (PowerShell)
│   └── activate.bat                # Активация (CMD)
│
├── 📁 NodeJS/                      # Node.js окружение
│   ├── global_modules/             # Глобальные npm пакеты
│   ├── .npmrc                      # npm конфигурация
│   └── setup_nodejs.ps1            # Установка Node.js окружения
│
├── 📁 Docker/                      # Docker конфигурация
│   ├── compose/                    # Docker Compose файлы
│   │   ├── postgres.yml            # PostgreSQL
│   │   ├── redis.yml               # Redis
│   │   ├── mongodb.yml             # MongoDB
│   │   ├── mysql.yml               # MySQL
│   │   └── fullstack.yml           # Все сервисы
│   ├── volumes/                    # Данные контейнеров
│   │   ├── postgres/
│   │   ├── redis/
│   │   ├── mongodb/
│   │   └── mysql/
│   ├── data/                       # Дополнительные данные
│   ├── setup_docker.ps1            # Установка Docker окружения
│   ├── start-all.ps1               # Запустить все контейнеры
│   ├── stop-all.ps1                # Остановить все контейнеры
│   └── status.ps1                  # Статус контейнеров
│
├── 📁 Git/                         # Git конфигурация
│   ├── config/                     # Шаблоны конфигураций
│   │   ├── .gitconfig              # Шаблон Git конфига
│   │   └── .gitignore              # Шаблон игнорируемых файлов
│   ├── setup_git.ps1               # Установка Git конфигурации
│   ├── setup-user.ps1              # Настройка пользователя Git
│   └── show-config.ps1             # Показать текущую конфигурацию
│
├── 📁 Database/                    # Локальные базы данных (SQLite и др.)
│
├── 📁 Scripts/                     # Утилиты и скрипты
│   ├── quick-python.ps1            # Быстрый запуск Python
│   ├── quick-pip.ps1               # Быстрый запуск pip
│   ├── quick-node.ps1              # Быстрый запуск Node.js
│   ├── backup-devtools.ps1         # Резервное копирование DevTools
│   └── update-all.ps1              # Обновление всех пакетов
│
├── 📁 Config/                      # Общие конфигурации
│   └── env.example                 # Шаблон переменных окружения
│
├── 📁 Docs/                        # Документация
│   └── STRUCTURE.md                # Этот файл
│
├── 📁 Utils/                       # Дополнительные утилиты
│
├── 📁 VSCode/                      # VSCode конфигурация и расширения
│
├── 📁 LM Studio/                   # LM Studio модели и конфигурация
│
├── 📁 Caches/                      # Кэши (npm, pip, и др.)
│   └── npm/                        # npm кэш
│
├── 📁 Installers/                  # Установочные файлы
│
├── 📁 Temp/                        # Временные файлы
│
├── 📁 voice/                       # Голосовые инструменты
│
├── 📄 DevTools-Manager.ps1         # ГЛАВНЫЙ МЕНЕДЖЕР
├── 📄 README.md                    # Основная документация
├── 📄 QUICKSTART.md                # Быстрый старт
│
└── 📄 Устаревшие скрипты:
    ├── ai_full_installer.ps1       # Старый AI установщик
    ├── ai_extra_setup.ps1          # Дополнительная AI настройка
    ├── ai_optimize.ps1             # AI оптимизация
    ├── run_whisper.py              # Python скрипт Whisper
    ├── voice_assistant.py          # Голосовой ассистент
    ├── whisper_from_file.py        # Whisper из файла
    ├── whisper_mic_realtime.py     # Whisper с микрофона
    └── win10_dev_ai_pro_smart_D.ps1 # Старый установщик
```

## Ключевые компоненты

### 1. DevTools-Manager.ps1
**Главный управляющий скрипт**

Команды:
- `setup <tool>` - Установка инструментов
- `status` - Статус всех инструментов
- `activate <env>` - Активация окружения
- `docker <cmd>` - Docker команды
- `help` - Справка

### 2. Python окружение
- Виртуальное окружение в `Python/venv/`
- Все пакеты изолированы от системного Python
- Легко переносимо и воспроизводимо

### 3. Node.js окружение
- Глобальные пакеты в `NodeJS/global_modules/`
- npm конфигурирован для использования локальных директорий
- Изолировано от системного Node.js

### 4. Docker конфигурация
- Готовые Compose файлы для популярных баз данных
- Данные хранятся в `Docker/volumes/`
- Удобные скрипты для управления контейнерами

### 5. Утилиты (Scripts/)
- `quick-*.ps1` - Быстрый запуск инструментов
- `backup-devtools.ps1` - Резервное копирование
- `update-all.ps1` - Обновление всех пакетов

## Зависимости между компонентами

```
DevTools-Manager.ps1
    ├── Python/setup_python.ps1
    ├── NodeJS/setup_nodejs.ps1
    ├── Docker/setup_docker.ps1
    └── Git/setup_git.ps1

Scripts/quick-python.ps1 → Python/venv/Scripts/python.exe
Scripts/quick-pip.ps1 → Python/venv/Scripts/python.exe
Scripts/quick-node.ps1 → NodeJS/global_modules/

Docker/start-all.ps1 → Docker/compose/fullstack.yml
```

## Путь данных

### Python пакеты
```
Установка: Python/venv/Lib/site-packages/
Скрипты: Python/venv/Scripts/
Кэш: %LOCALAPPDATA%\pip\Cache
```

### Node.js пакеты
```
Глобальные: NodeJS/global_modules/
Кэш: Caches/npm/
```

### Docker данные
```
Конфигурация: Docker/compose/
Данные: Docker/volumes/
```

## Переносимость

### Что можно переносить:
- ✅ Всю папку `D:\DevTools`
- ✅ Python venv (после переустановки путей)
- ✅ Node.js global_modules
- ✅ Docker compose файлы
- ✅ Все скрипты и конфигурации

### Что НЕ переносится:
- ❌ Docker volumes (нужно экспортировать данные)
- ❌ Системный Python/Node.js
- ❌ Некоторые скомпилированные Python пакеты

### Процесс переноса:
1. Скопировать `D:\DevTools` на новую машину
2. Запустить `.\DevTools-Manager.ps1 setup all`
3. Перенастроить Git user: `.\Git\setup-user.ps1`

## Размеры (примерно)

```
Python/venv/          ~500MB  (зависит от пакетов)
NodeJS/global_modules/ ~200MB  (зависит от пакетов)
Docker/volumes/       ~100MB+ (зависит от данных)
AI/env/              ~3-5GB  (если установлен)
Скрипты и конфиги    ~5MB
```

## Безопасность

### Файлы с секретами (НЕ коммитить!):
- `.env` файлы
- `*password*` файлы
- `*secret*` файлы
- `Docker/volumes/*` (могут содержать данные БД)

### Git ignore шаблон:
См. `Git/config/.gitignore`

## Обслуживание

### Регулярные задачи:

**Еженедельно:**
```powershell
.\Scripts\update-all.ps1  # Обновить все пакеты
```

**Ежемесячно:**
```powershell
.\Scripts\backup-devtools.ps1  # Создать бэкап
```

**По необходимости:**
```powershell
.\DevTools-Manager.ps1 status  # Проверить статус
```

## Расширение

### Добавление новых инструментов:

1. Создайте папку в `DevTools/`
2. Создайте `setup_<tool>.ps1`
3. Добавьте команду в `DevTools-Manager.ps1`
4. Обновите документацию

### Пример:
```
DevTools/
├── NewTool/
│   ├── setup_newtool.ps1
│   └── config/
```

## Полезные ссылки

- [README.md](../README.md) - Основная документация
- [QUICKSTART.md](../QUICKSTART.md) - Быстрый старт
- [Config/env.example](../Config/env.example) - Шаблон переменных окружения

---

**Дата обновления:** 2025-12-04
**Версия:** 1.0
