"""Handlers for bot control commands (pause/resume)."""

from telegram import Update
from telegram.ext import ContextTypes

from src.admin.handlers.common import is_admin


async def pause_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /pause command - pause bot operations."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    monitor = context.bot_data.get("monitor")
    messenger = context.bot_data.get("messenger")

    if monitor:
        monitor.pause()
    if messenger:
        messenger.pause()

    await update.message.reply_text("Bot paused. Comment monitoring and message sending stopped.")


async def resume_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /resume command - resume bot operations."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    monitor = context.bot_data.get("monitor")
    messenger = context.bot_data.get("messenger")

    if monitor:
        monitor.resume()
    if messenger:
        messenger.resume()

    await update.message.reply_text("Bot resumed. Comment monitoring and message sending active.")
