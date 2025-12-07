"""Handlers for message template management commands."""

from telegram import Update
from telegram.ext import ContextTypes

from src.admin.handlers.common import is_admin


async def list_templates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /templates command - list all templates."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    repository = context.bot_data.get("repository")
    templates = await repository.get_all_templates()

    if not templates:
        await update.message.reply_text("No templates added yet.")
        return

    text = "*Message Templates:*\n\n"
    for tpl in templates:
        # Truncate long content
        content_preview = tpl.content[:100] + "..." if len(tpl.content) > 100 else tpl.content
        text += f"ID: {tpl.id}\n"
        text += f"Name: `{tpl.name}`\n"
        text += f"Content: {content_preview}\n\n"

    text += "_Variables: {username}, {post\\_url}, {keyword}_"

    await update.message.reply_text(text, parse_mode="Markdown")


async def add_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /add_template command - add new template.

    Usage: /add_template <name> | <content>
    """
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    # Get full message text after command
    if not update.message.text:
        await update.message.reply_text(
            "Usage: /add\\_template <name> | <content>\n"
            "Variables: {username}, {post\\_url}, {keyword}",
            parse_mode="Markdown",
        )
        return

    # Extract text after /add_template
    text = update.message.text
    if " " not in text:
        await update.message.reply_text(
            "Usage: /add\\_template <name> | <content>\n"
            "Variables: {username}, {post\\_url}, {keyword}",
            parse_mode="Markdown",
        )
        return

    args_text = text.split(" ", 1)[1]

    if "|" not in args_text:
        await update.message.reply_text(
            "Please separate name and content with |\n"
            "Example: /add\\_template Welcome | Hi {username}!",
            parse_mode="Markdown",
        )
        return

    parts = args_text.split("|", 1)
    name = parts[0].strip()
    content = parts[1].strip()

    if not name or not content:
        await update.message.reply_text("Name and content cannot be empty.")
        return

    repository = context.bot_data.get("repository")
    template = await repository.add_template(name, content)

    await update.message.reply_text(
        f"Template added (ID: {template.id})\nName: `{template.name}`",
        parse_mode="Markdown",
    )


async def preview_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /preview_template command - preview template with sample data."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /preview\\_template <id>", parse_mode="Markdown")
        return

    try:
        template_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID must be a number.")
        return

    repository = context.bot_data.get("repository")
    template = await repository.get_template_by_id(template_id)

    if not template:
        await update.message.reply_text("Template not found.")
        return

    # Preview with sample data
    preview = template.content.format(
        username="sample_user",
        post_url="https://instagram.com/p/ABC123",
        keyword="KEYWORD",
    )

    await update.message.reply_text(
        f"*Template Preview:*\n\n{preview}",
        parse_mode="Markdown",
    )
