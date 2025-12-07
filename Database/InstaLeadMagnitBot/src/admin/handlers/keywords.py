"""Handlers for keyword management commands."""

from telegram import Update
from telegram.ext import ContextTypes

from src.admin.handlers.common import is_admin


async def list_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /keywords command - list all keywords."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    repository = context.bot_data.get("repository")
    keywords = await repository.get_all_keywords()

    if not keywords:
        await update.message.reply_text("No keywords added yet.")
        return

    text = "*Keywords:*\n\n"
    for kw in keywords:
        status = "[ON]" if kw.is_active else "[OFF]"
        text += f"{status} ID: {kw.id}\n"
        text += f"   Word: `{kw.word}`\n"
        text += f"   Match: {kw.match_type.value}\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def add_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /add_keyword command - add new keyword.

    Usage: /add_keyword <word> [match_type]
    Match types: exact, contains (default), regex
    """
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /add\\_keyword <word> [match\\_type]\n"
            "Match types: exact, contains (default), regex",
            parse_mode="Markdown",
        )
        return

    word = context.args[0].lower()
    match_type = context.args[1].lower() if len(context.args) > 1 else "contains"

    if match_type not in ("exact", "contains", "regex"):
        await update.message.reply_text("Invalid match type. Use: exact, contains, regex")
        return

    repository = context.bot_data.get("repository")

    # Check for duplicate
    existing = await repository.get_keyword_by_word(word)
    if existing:
        await update.message.reply_text(f"Keyword already exists (ID: {existing.id})")
        return

    # Invalidate matcher cache
    matcher = context.bot_data.get("matcher")
    if matcher:
        matcher.invalidate_cache()

    keyword = await repository.add_keyword(word, match_type)
    await update.message.reply_text(
        f"Keyword added (ID: {keyword.id})\nWord: `{keyword.word}`\nMatch: {match_type}",
        parse_mode="Markdown",
    )


async def remove_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /remove_keyword command - toggle keyword."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /remove\\_keyword <id>", parse_mode="Markdown")
        return

    try:
        keyword_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID must be a number.")
        return

    repository = context.bot_data.get("repository")
    result = await repository.toggle_keyword(keyword_id)

    # Invalidate matcher cache
    matcher = context.bot_data.get("matcher")
    if matcher:
        matcher.invalidate_cache()

    if result is not None:
        status = "activated" if result else "deactivated"
        await update.message.reply_text(f"Keyword {keyword_id} {status}")
    else:
        await update.message.reply_text("Keyword not found.")
