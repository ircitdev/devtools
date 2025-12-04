---
description: Создание миграции БД (Alembic)
---

Создай миграцию базы данных используя Alembic.

Включи:
- Alembic migration file
- upgrade() функция
- downgrade() функция для rollback
- Правильные типы столбцов
- Constraints (FK, unique, not null)
- Indexes где нужно
- Комментарий что изменяется

Команды для применения:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1  # rollback
```

Проверь что миграция безопасна и обратима.
