"""Handlers for rule management commands."""

from telegram import Update
from telegram.ext import ContextTypes

from src.admin.handlers.common import is_admin


async def list_rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /rules command - list all rules."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    repository = context.bot_data.get("repository")
    rules = await repository.get_all_rules()

    if not rules:
        await update.message.reply_text("No rules added yet.")
        return

    text = "*Rules:*\n\n"
    for rule in rules:
        status = "[ON]" if rule.is_active else "[OFF]"
        keyword_name = rule.keyword.word if rule.keyword else "N/A"
        template_name = rule.template.name if rule.template else "N/A"
        post_info = f"Post {rule.post_id}" if rule.post_id else "All posts"

        text += f"{status} ID: {rule.id}\n"
        text += f"   Keyword: `{keyword_name}`\n"
        text += f"   Template: `{template_name}`\n"
        text += f"   Scope: {post_info}\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def add_rule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /add_rule command - add new rule.

    Usage: /add_rule <keyword_id> <template_id> [post_id]
    If post_id is omitted, rule applies to all posts.
    """
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /add\\_rule <keyword\\_id> <template\\_id> [post\\_id]\n"
            "Omit post\\_id to apply to all posts.",
            parse_mode="Markdown",
        )
        return

    try:
        keyword_id = int(context.args[0])
        template_id = int(context.args[1])
        post_id = int(context.args[2]) if len(context.args) > 2 else None
    except ValueError:
        await update.message.reply_text("IDs must be numbers.")
        return

    repository = context.bot_data.get("repository")

    # Verify keyword exists
    keywords = await repository.get_all_keywords()
    if not any(k.id == keyword_id for k in keywords):
        await update.message.reply_text(f"Keyword {keyword_id} not found.")
        return

    # Verify template exists
    template = await repository.get_template_by_id(template_id)
    if not template:
        await update.message.reply_text(f"Template {template_id} not found.")
        return

    # Verify post exists if specified
    if post_id:
        post = await repository.get_post_by_id(post_id)
        if not post:
            await update.message.reply_text(f"Post {post_id} not found.")
            return

    # Invalidate matcher cache
    matcher = context.bot_data.get("matcher")
    if matcher:
        matcher.invalidate_cache()

    rule = await repository.add_rule(keyword_id, template_id, post_id)

    scope = f"post {post_id}" if post_id else "all posts"
    await update.message.reply_text(
        f"Rule added (ID: {rule.id})\n"
        f"Keyword ID: {keyword_id}\n"
        f"Template ID: {template_id}\n"
        f"Scope: {scope}",
    )


async def toggle_rule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /toggle_rule command - toggle rule active status."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /toggle\\_rule <id>", parse_mode="Markdown")
        return

    try:
        rule_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID must be a number.")
        return

    repository = context.bot_data.get("repository")
    result = await repository.toggle_rule(rule_id)

    # Invalidate matcher cache
    matcher = context.bot_data.get("matcher")
    if matcher:
        matcher.invalidate_cache()

    if result is not None:
        status = "activated" if result else "deactivated"
        await update.message.reply_text(f"Rule {rule_id} {status}")
    else:
        await update.message.reply_text("Rule not found.")
