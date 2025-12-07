# InstaLeadMagnitBot

Instagram Lead Magnet Bot - автоматическая система лидогенерации через Instagram. Мониторит комментарии под постами, отслеживает ключевые слова и отправляет персонализированные сообщения в Direct.

## Возможности

- **Мониторинг комментариев** - автоматическое отслеживание комментариев под выбранными постами
- **Ключевые слова** - триггеры для отправки сообщений (exact/contains/regex)
- **Шаблоны сообщений** - персонализированные сообщения с переменными
- **Правила** - гибкая связка "ключевое слово → шаблон → пост"
- **Welcome-сообщения** - автоматические приветствия новым подписчикам
- **Массовые рассылки** - broadcast по сегментам пользователей
- **Google Sheets логирование** - запись всех событий в таблицу
- **Telegram-бот** - полное управление через Telegram

## Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                       main.py                                │
│        (Инициализация, event loop, координация)             │
└─────────────────────────────────────────────────────────────┘
         │           │           │           │           │
         ▼           ▼           ▼           ▼           ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Telegram Bot │ │ Comment  │ │ Direct   │ │ Follower │ │Broadcast │
│ (admin/bot)  │ │ Monitor  │ │ Messenger│ │ Monitor  │ │ Manager  │
└──────────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Google Sheets Logger        │
              └───────────────────────────────┘
```

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/ircitdev/devtools.git
cd InstaLeadMagnitBot
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка конфигурации

Скопируйте `.env.example` в `.env` и заполните:

```env
# Instagram
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
INSTAGRAM_SESSION_FILE=session.json

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
ADMIN_TELEGRAM_IDS=123456789

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/bot.db

# Rate Limiting
CHECK_INTERVAL_SECONDS=60
MESSAGE_DELAY_MIN_SECONDS=30
MESSAGE_DELAY_MAX_SECONDS=60
MAX_MESSAGES_PER_HOUR=50

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# Google Sheets (опционально)
GOOGLE_SHEETS_ENABLED=true
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id
```

### 5. Настройка Google Sheets (опционально)

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Google Sheets API
3. Создайте Service Account и скачайте JSON-ключ
4. Поместите файл как `credentials.json` в корень проекта
5. Откройте доступ к таблице для email сервисного аккаунта

### 6. Запуск

```bash
python run.py
```

## Команды Telegram-бота

### Основные

| Команда | Описание |
|---------|----------|
| `/start` | Показать меню команд |
| `/status` | Статус бота и статистика |
| `/pause` | Приостановить мониторинг |
| `/resume` | Возобновить мониторинг |

### Посты

| Команда | Описание |
|---------|----------|
| `/posts` | Список отслеживаемых постов |
| `/add_post <url>` | Добавить пост |
| `/remove_post <id>` | Удалить пост |

### Ключевые слова

| Команда | Описание |
|---------|----------|
| `/keywords` | Список ключевых слов |
| `/add_keyword <word>` | Добавить слово |
| `/remove_keyword <id>` | Удалить слово |

### Шаблоны сообщений

| Команда | Описание |
|---------|----------|
| `/templates` | Список шаблонов |
| `/add_template <name> \| <text>` | Добавить шаблон |
| `/preview_template <id>` | Предпросмотр |

**Переменные в шаблонах:**
- `{username}` - имя пользователя
- `{post_url}` - URL поста
- `{keyword}` - сработавшее ключевое слово

### Правила

| Команда | Описание |
|---------|----------|
| `/rules` | Список правил |
| `/add_rule <keyword_id> <template_id> [post_id]` | Создать правило |
| `/toggle_rule <id>` | Вкл/выкл правило |

### Welcome-сообщения (новые подписчики)

| Команда | Описание |
|---------|----------|
| `/welcome` | Настройки приветствий |
| `/set_welcome <text>` | Установить текст приветствия |
| `/toggle_welcome` | Включить/выключить |

### Массовые рассылки (Broadcasts)

| Команда | Описание |
|---------|----------|
| `/broadcasts` | Список рассылок |
| `/segments` | Доступные сегменты с количеством пользователей |
| `/broadcast keyword <id> \| <name> \| <message>` | Рассылка по ключевому слову |
| `/broadcast followers <days> \| <name> \| <message>` | Рассылка новым подписчикам |
| `/broadcast all \| <name> \| <message>` | Рассылка всем комментаторам |
| `/broadcast_status <id>` | Статус рассылки |
| `/pause_broadcast <id>` | Приостановить |
| `/resume_broadcast <id>` | Продолжить |
| `/cancel_broadcast <id>` | Отменить |

## Пример использования

### Базовый сценарий

1. **Добавить пост:**
   ```
   /add_post https://instagram.com/p/ABC123
   ```

2. **Добавить ключевое слово:**
   ```
   /add_keyword ГАЙД
   ```

3. **Создать шаблон:**
   ```
   /add_template Приветствие | Привет, {username}! Держи гайд: https://example.com
   ```

4. **Создать правило:**
   ```
   /add_rule 1 1
   ```

Теперь когда кто-то напишет "ГАЙД" в комментарии, бот отправит ему DM.

### Welcome-сообщения

```
/set_welcome Привет, {username}! Спасибо за подписку! Вот ссылка на бесплатные материалы: https://example.com
/toggle_welcome
```

### Массовая рассылка

```
/segments
/broadcast followers 7 | Акция | Привет {username}! Только для подписчиков - скидка 50%!
```

## Структура проекта

```
InstaLeadMagnitBot/
├── src/
│   ├── __init__.py
│   ├── main.py                  # Главный модуль
│   ├── config.py                # Конфигурация
│   ├── instagram/
│   │   ├── client.py            # Instagram API клиент
│   │   ├── monitor.py           # Мониторинг комментариев
│   │   ├── messenger.py         # Отправка DM
│   │   ├── follower_monitor.py  # Мониторинг подписчиков
│   │   └── broadcast_manager.py # Массовые рассылки
│   ├── core/
│   │   ├── matcher.py           # Поиск ключевых слов
│   │   └── rules.py             # Движок правил
│   ├── database/
│   │   ├── models.py            # SQLAlchemy модели
│   │   └── repository.py        # CRUD операции
│   ├── admin/
│   │   ├── bot.py               # Telegram бот
│   │   └── handlers/            # Обработчики команд
│   │       ├── common.py
│   │       ├── posts.py
│   │       ├── keywords.py
│   │       ├── templates.py
│   │       ├── rules.py
│   │       ├── control.py
│   │       ├── welcome.py
│   │       └── broadcasts.py
│   └── utils/
│       ├── helpers.py           # Утилиты
│       └── sheets_logger.py     # Google Sheets логгер
├── data/                        # База данных
├── logs/                        # Логи
├── .env                         # Конфигурация
├── .env.example                 # Пример конфигурации
├── credentials.json             # Google API ключ
├── requirements.txt
└── run.py                       # Точка входа
```

## Google Sheets логирование

При включенном логировании автоматически создаются вкладки:

| Вкладка | Содержимое |
|---------|------------|
| Events | Запуск, остановка, изменения конфигурации |
| SentMessages | Отправленные DM |
| NewFollowers | Новые подписчики |
| Comments | Обработанные комментарии |
| Errors | Ошибки |
| Broadcasts | Массовые рассылки |

## Rate Limiting

Для защиты от блокировки Instagram:

| Параметр | Значение |
|----------|----------|
| Проверка комментариев | каждые 60 сек |
| Задержка между DM | 30-60 сек |
| Лимит DM | 50/час |
| Задержка broadcast | 45-90 сек |
| Лимит broadcast | 30/час |

## Модели данных

| Модель | Описание |
|--------|----------|
| Post | Отслеживаемый пост |
| Keyword | Ключевое слово (exact/contains/regex) |
| MessageTemplate | Шаблон сообщения |
| Rule | Связка keyword → template → post |
| SentMessage | Лог отправленных сообщений |
| ProcessedComment | Обработанные комментарии |
| WelcomeSettings | Настройки приветствий |
| ProcessedFollower | Приветствованные подписчики |
| Broadcast | Кампания рассылки |
| BroadcastRecipient | Получатели рассылки |

## Технологии

- **Python 3.11+**
- **instagrapi** - Instagram Private API
- **python-telegram-bot 20.x** - Async Telegram Bot
- **SQLAlchemy 2.0 + aiosqlite** - Async ORM
- **gspread** - Google Sheets API
- **pydantic-settings** - Конфигурация
- **loguru** - Логирование

## Безопасность

- Храните `.env` и `credentials.json` в секрете
- Не коммитьте файлы с паролями
- Используйте отдельный Instagram аккаунт
- Соблюдайте rate limits
- Добавьте файлы в `.gitignore`

## Лицензия

MIT License
