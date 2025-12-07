# InstaLeadMagnitBot - Инструкции для разработки

## Описание проекта

Instagram бот для автоматической лидогенерации. Отслеживает ключевые слова в комментариях к постам и отправляет персонализированные сообщения в Direct.

## Ключевые требования

### Функциональность
- Мониторинг комментариев к указанным постам в реальном времени
- Обнаружение ключевых слов (exact/contains/regex)
- Автоматическая отправка сообщений в Direct
- Telegram-бот для администрирования
- Статистика и аналитика

### Безопасность
- Соблюдение лимитов Instagram API (50-100 DM/час)
- Задержки между сообщениями (30-60 сек)
- Защита от повторной обработки комментариев
- Хранение credentials в .env

## Структура проекта

```
src/
├── main.py              # Точка входа
├── config.py            # Конфигурация
├── instagram/           # Instagram API
│   ├── client.py        # API клиент
│   ├── monitor.py       # Мониторинг комментариев
│   └── messenger.py     # Отправка Direct
├── core/                # Бизнес-логика
│   ├── rules.py         # Движок правил
│   ├── matcher.py       # Сопоставление слов
│   └── scheduler.py     # Планировщик
├── database/            # База данных
│   ├── models.py        # SQLAlchemy модели
│   └── repository.py    # Репозитории
├── admin/               # Админ-панель
│   ├── bot.py           # Telegram бот
│   └── handlers/        # Обработчики команд
└── utils/               # Утилиты
```

## Стандарты кода

- Python 3.11+
- Форматирование: Black
- Линтер: Ruff
- Type hints везде
- Docstrings для публичных методов
- Логирование через loguru

## Важные библиотеки

- `instagrapi` - Instagram Private API
- `python-telegram-bot` - Telegram Bot API
- `SQLAlchemy` - ORM
- `Celery` - очередь задач
- `loguru` - логирование

## Переменные окружения

Обязательные:
- INSTAGRAM_USERNAME
- INSTAGRAM_PASSWORD
- TELEGRAM_BOT_TOKEN
- ADMIN_TELEGRAM_IDS

Опциональные:
- DATABASE_URL (default: sqlite:///./bot.db)
- CHECK_INTERVAL_SECONDS (default: 60)
- MESSAGE_DELAY_SECONDS (default: 45)
- MAX_MESSAGES_PER_HOUR (default: 50)

## Модели данных

### Post
- instagram_id, url, is_active, created_at

### Keyword
- word, match_type (exact/contains/regex), is_active

### MessageTemplate
- name, content (с переменными {username}, {post_url}, {keyword})

### Rule
- post_id, keyword_id, template_id, cooldown_hours, is_active

### SentMessage
- user_id, username, post_id, rule_id, sent_at, status

## Команды Telegram-бота

- /start, /status - общие
- /posts, /add_post, /remove_post - посты
- /keywords, /add_keyword, /remove_keyword - слова
- /templates, /add_template, /edit_template - шаблоны
- /rules, /add_rule, /toggle_rule - правила
- /pause, /resume, /logs - управление
