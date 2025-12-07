"""Telegram handlers for welcome message management."""

from telegram import Update
from telegram.ext import ContextTypes

from src.admin.handlers.common import is_admin


async def welcome_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show welcome message settings. Usage: /welcome"""
    if not await is_admin(update, context):
        return

    repository = context.bot_data["repository"]
    settings = await repository.get_welcome_settings()

    if not settings:
        await update.message.reply_text(
            "Приветственные сообщения не настроены.\n\n"
            "Используйте:\n"
            "/set_welcome <текст> - установить сообщение\n"
            "/toggle_welcome - вкл/выкл\n\n"
            "В тексте можно использовать {username}"
        )
        return

    status = "включены" if settings.is_enabled else "выключены"
    message_preview = settings.message[:100] + "..." if len(settings.message) > 100 else settings.message

    welcomed_count = await repository.get_welcomed_followers_count()

    await update.message.reply_text(
        f"Приветственные сообщения: {status}\n\n"
        f"Текст сообщения:\n{message_preview}\n\n"
        f"Отправлено приветствий: {welcomed_count}\n\n"
        "Команды:\n"
        "/set_welcome <текст> - изменить сообщение\n"
        "/toggle_welcome - вкл/выкл"
    )


async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set welcome message text. Usage: /set_welcome <message>"""
    if not await is_admin(update, context):
        return

    if not context.args:
        await update.message.reply_text(
            "Укажите текст приветствия.\n\n"
            "Пример: /set_welcome Привет, {username}! Спасибо за подписку!"
        )
        return

    message = " ".join(context.args)
    repository = context.bot_data["repository"]

    await repository.set_welcome_message(message)

    await update.message.reply_text(
        f"Приветственное сообщение установлено:\n\n{message}\n\n"
        "Используйте /toggle_welcome для включения."
    )


async def toggle_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Toggle welcome messages on/off. Usage: /toggle_welcome"""
    if not await is_admin(update, context):
        return

    repository = context.bot_data["repository"]
    settings = await repository.get_welcome_settings()

    if not settings or not settings.message:
        await update.message.reply_text(
            "Сначала установите текст приветствия:\n"
            "/set_welcome <текст сообщения>"
        )
        return

    new_status = await repository.toggle_welcome()
    status = "ВКЛЮЧЕНЫ" if new_status else "ВЫКЛЮЧЕНЫ"

    await update.message.reply_text(f"Приветственные сообщения {status}")
