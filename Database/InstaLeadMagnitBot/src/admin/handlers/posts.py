"""Handlers for post management commands."""

from telegram import Update
from telegram.ext import ContextTypes

from src.utils.helpers import extract_post_id_from_url
from src.admin.handlers.common import is_admin


async def list_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /posts command - list all posts."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    repository = context.bot_data.get("repository")
    posts = await repository.get_all_posts()

    if not posts:
        await update.message.reply_text("No posts added yet.")
        return

    text = "*Monitored Posts:*\n\n"
    for post in posts:
        status = "[ON]" if post.is_active else "[OFF]"
        text += f"{status} ID: {post.id}\n"
        text += f"   Instagram: `{post.instagram_id}`\n"
        text += f"   {post.url}\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def add_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /add_post command - add new post."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /add\\_post <url>", parse_mode="Markdown")
        return

    url = context.args[0]
    instagram_id = extract_post_id_from_url(url)

    if not instagram_id:
        await update.message.reply_text("Could not extract post ID from URL.")
        return

    repository = context.bot_data.get("repository")

    # Check for duplicate
    existing = await repository.get_post_by_instagram_id(instagram_id)
    if existing:
        await update.message.reply_text(f"Post already exists (ID: {existing.id})")
        return

    post = await repository.add_post(instagram_id, url)
    await update.message.reply_text(f"Post added (ID: {post.id})")


async def remove_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /remove_post command - toggle or remove post."""
    if not is_admin(update, context):
        await update.message.reply_text("Access denied.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /remove\\_post <id>", parse_mode="Markdown")
        return

    try:
        post_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID must be a number.")
        return

    repository = context.bot_data.get("repository")
    result = await repository.toggle_post(post_id)

    if result is not None:
        status = "activated" if result else "deactivated"
        await update.message.reply_text(f"Post {post_id} {status}")
    else:
        await update.message.reply_text("Post not found.")
