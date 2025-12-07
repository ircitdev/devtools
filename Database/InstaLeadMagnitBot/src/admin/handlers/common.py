"""Common handlers for start and status commands."""

from telegram import Update
from telegram.ext import ContextTypes


def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if user is admin.

    Args:
        update: Telegram update
        context: Bot context

    Returns:
        True if user is admin
    """
    admin_ids = context.bot_data.get("admin_ids", [])
    return update.effective_user.id in admin_ids


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    welcome_text = """
*InstaLeadMagnitBot - Admin Panel*

*Posts:*
/posts - List monitored posts
/add\\_post <url> - Add post
/remove\\_post <id> - Remove post

*Keywords:*
/keywords - List keywords
/add\\_keyword <word> - Add keyword
/remove\\_keyword <id> - Remove keyword

*Templates:*
/templates - List templates
/add\\_template <name> | <text> - Add template

*Rules:*
/rules - List rules
/add\\_rule <keyword\\_id> <template\\_id> [post\\_id]
/toggle\\_rule <id> - Toggle rule

*Welcome (new followers):*
/welcome - View settings
/set\\_welcome <text> - Set message
/toggle\\_welcome - On/Off

*Broadcasts (mass DM):*
/broadcasts - List broadcasts
/segments - Show segments with user counts
/broadcast <type> | <name> | <message>
/broadcast\\_status <id> - Broadcast progress
/pause\\_broadcast <id> - Pause
/resume\\_broadcast <id> - Resume
/cancel\\_broadcast <id> - Cancel

*Control:*
/status - Bot status
/pause - Pause bot
/resume - Resume bot
"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    repository = context.bot_data.get("repository")
    messenger = context.bot_data.get("messenger")
    monitor = context.bot_data.get("monitor")

    if not repository:
        await update.message.reply_text("Bot not initialized.")
        return

    stats = await repository.get_stats()

    # Determine bot state
    is_paused = False
    if monitor:
        is_paused = monitor.is_paused

    queue_size = messenger.queue_size if messenger else 0

    status_emoji = "Paused" if is_paused else "Running"

    status_text = f"""
*Bot Status*

State: {status_emoji}

*Statistics:*
- Posts monitored: {stats['active_posts']} / {stats['total_posts']}
- Keywords: {stats['total_keywords']}
- Templates: {stats['total_templates']}
- Rules: {stats['total_rules']}
- Comments processed: {stats['total_comments_processed']}
- Messages sent: {stats['total_sent']}
- Sent last hour: {stats['sent_last_hour']}

Queue: {queue_size}
"""
    await update.message.reply_text(status_text, parse_mode="Markdown")
