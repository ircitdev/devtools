"""Handlers for broadcast management commands."""

from telegram import Update
from telegram.ext import ContextTypes

from src.admin.handlers.common import is_admin


async def list_broadcasts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /broadcasts command - list all broadcasts."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    repository = context.bot_data.get("repository")
    if not repository:
        await update.message.reply_text("Bot not initialized.")
        return

    broadcasts = await repository.get_all_broadcasts()

    if not broadcasts:
        await update.message.reply_text("No broadcasts found.")
        return

    status_icons = {
        "pending": "⏳",
        "in_progress": "▶️",
        "paused": "⏸",
        "completed": "✅",
        "cancelled": "❌",
    }

    text = "*Broadcasts:*\n\n"
    for b in broadcasts[:10]:  # Show last 10
        icon = status_icons.get(b.status.value, "❓")
        progress = f"{b.sent_count}/{b.total_users}" if b.total_users > 0 else "0/0"
        text += f"{icon} *{b.id}.* {b.name}\n"
        text += f"   Segment: {b.segment_type.value}\n"
        text += f"   Progress: {progress} (failed: {b.failed_count})\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def create_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /broadcast command - create and start a new broadcast.

    Usage:
    /broadcast keyword <keyword_id> | <name> | <message>
    /broadcast followers <days> | <name> | <message>
    /broadcast all | <name> | <message>
    """
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    broadcast_manager = context.bot_data.get("broadcast_manager")
    if not broadcast_manager:
        await update.message.reply_text("Broadcast manager not initialized.")
        return

    args = " ".join(context.args) if context.args else ""

    if not args:
        help_text = """*Create Broadcast:*

/broadcast keyword <id> | <name> | <message>
Send to users who commented with keyword

/broadcast followers <days> | <name> | <message>
Send to new followers from last N days

/broadcast all | <name> | <message>
Send to all commenters

*Example:*
/broadcast keyword 1 | Promo | Hi {username}! Check our new offer!

*Variables:*
{username} - will be replaced with user's name
"""
        await update.message.reply_text(help_text, parse_mode="Markdown")
        return

    try:
        # Parse command
        parts = args.split("|")
        if len(parts) < 2:
            await update.message.reply_text("Invalid format. Use: /broadcast <type> | <name> | <message>")
            return

        segment_part = parts[0].strip()
        name = parts[1].strip() if len(parts) > 1 else "Broadcast"
        message = parts[2].strip() if len(parts) > 2 else parts[1].strip()

        # Determine segment type
        segment_words = segment_part.split()
        segment_type = segment_words[0].lower()
        segment_filter = segment_words[1] if len(segment_words) > 1 else None

        if segment_type == "keyword":
            if not segment_filter:
                await update.message.reply_text("Specify keyword ID: /broadcast keyword <id> | ...")
                return
            segment_type = "keyword_commenters"
        elif segment_type == "followers":
            segment_type = "new_followers"
            segment_filter = segment_filter or "7"
        elif segment_type == "all":
            segment_type = "all_commenters"
            segment_filter = None
        else:
            await update.message.reply_text("Unknown segment type. Use: keyword, followers, or all")
            return

        # Create and start broadcast
        await update.message.reply_text(f"Creating broadcast '{name}'...")

        broadcast_id = await broadcast_manager.create_and_start_broadcast(
            name=name,
            message=message,
            segment_type=segment_type,
            segment_filter=segment_filter,
        )

        if broadcast_id:
            await update.message.reply_text(
                f"✅ Broadcast #{broadcast_id} started!\n"
                f"Use /broadcast\\_status {broadcast_id} to check progress."
            )
        else:
            await update.message.reply_text("❌ Failed to create broadcast. No users found for this segment.")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


async def broadcast_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /broadcast_status <id> - get broadcast status."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    repository = context.bot_data.get("repository")
    if not repository:
        await update.message.reply_text("Bot not initialized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast\\_status <id>")
        return

    try:
        broadcast_id = int(context.args[0])
        broadcast = await repository.get_broadcast(broadcast_id)

        if not broadcast:
            await update.message.reply_text(f"Broadcast #{broadcast_id} not found.")
            return

        status_icons = {
            "pending": "⏳ Pending",
            "in_progress": "▶️ In Progress",
            "paused": "⏸ Paused",
            "completed": "✅ Completed",
            "cancelled": "❌ Cancelled",
        }

        progress_pct = (
            (broadcast.sent_count / broadcast.total_users * 100)
            if broadcast.total_users > 0
            else 0
        )

        text = f"""*Broadcast #{broadcast.id}*

Name: {broadcast.name}
Status: {status_icons.get(broadcast.status.value, broadcast.status.value)}
Segment: {broadcast.segment_type.value}
Filter: {broadcast.segment_filter or 'N/A'}

*Progress:*
Total: {broadcast.total_users}
Sent: {broadcast.sent_count} ({progress_pct:.1f}%)
Failed: {broadcast.failed_count}
Remaining: {broadcast.total_users - broadcast.sent_count - broadcast.failed_count}

Created: {broadcast.created_at.strftime('%Y-%m-%d %H:%M')}
"""
        if broadcast.started_at:
            text += f"Started: {broadcast.started_at.strftime('%Y-%m-%d %H:%M')}\n"
        if broadcast.completed_at:
            text += f"Completed: {broadcast.completed_at.strftime('%Y-%m-%d %H:%M')}\n"

        await update.message.reply_text(text, parse_mode="Markdown")

    except ValueError:
        await update.message.reply_text("Invalid broadcast ID.")


async def pause_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /pause_broadcast <id> - pause a broadcast."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    broadcast_manager = context.bot_data.get("broadcast_manager")
    if not broadcast_manager:
        await update.message.reply_text("Broadcast manager not initialized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /pause\\_broadcast <id>")
        return

    try:
        broadcast_id = int(context.args[0])
        success = await broadcast_manager.pause_broadcast(broadcast_id)

        if success:
            await update.message.reply_text(f"⏸ Broadcast #{broadcast_id} paused.")
        else:
            await update.message.reply_text(f"Failed to pause broadcast #{broadcast_id}.")

    except ValueError:
        await update.message.reply_text("Invalid broadcast ID.")


async def resume_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /resume_broadcast <id> - resume a paused broadcast."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    broadcast_manager = context.bot_data.get("broadcast_manager")
    if not broadcast_manager:
        await update.message.reply_text("Broadcast manager not initialized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /resume\\_broadcast <id>")
        return

    try:
        broadcast_id = int(context.args[0])
        success = await broadcast_manager.resume_broadcast(broadcast_id)

        if success:
            await update.message.reply_text(f"▶️ Broadcast #{broadcast_id} resumed.")
        else:
            await update.message.reply_text(f"Failed to resume broadcast #{broadcast_id}.")

    except ValueError:
        await update.message.reply_text("Invalid broadcast ID.")


async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel_broadcast <id> - cancel a broadcast."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    broadcast_manager = context.bot_data.get("broadcast_manager")
    if not broadcast_manager:
        await update.message.reply_text("Broadcast manager not initialized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /cancel\\_broadcast <id>")
        return

    try:
        broadcast_id = int(context.args[0])
        success = await broadcast_manager.cancel_broadcast(broadcast_id)

        if success:
            await update.message.reply_text(f"❌ Broadcast #{broadcast_id} cancelled.")
        else:
            await update.message.reply_text(f"Failed to cancel broadcast #{broadcast_id}.")

    except ValueError:
        await update.message.reply_text("Invalid broadcast ID.")


async def list_segments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /segments command - show available segments with user counts."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    repository = context.bot_data.get("repository")
    if not repository:
        await update.message.reply_text("Bot not initialized.")
        return

    # Get counts
    all_commenters = await repository.get_all_commenters()
    recent_followers = await repository.get_recent_followers(7)
    keywords = await repository.get_all_keywords()

    text = "*Available Segments:*\n\n"

    text += f"*All Commenters:* {len(all_commenters)} users\n"
    text += f"*New Followers (7 days):* {len(recent_followers)} users\n\n"

    text += "*By Keyword:*\n"
    for kw in keywords[:10]:
        users = await repository.get_users_by_keyword(kw.id)
        text += f"  {kw.id}. {kw.word}: {len(users)} users\n"

    text += "\n*Usage:*\n"
    text += "/broadcast keyword <id> | name | message\n"
    text += "/broadcast followers <days> | name | message\n"
    text += "/broadcast all | name | message\n"

    await update.message.reply_text(text, parse_mode="Markdown")
