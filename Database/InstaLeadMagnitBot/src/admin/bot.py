"""Telegram admin bot for managing InstaLeadMagnitBot."""

from typing import TYPE_CHECKING, List, Optional

from loguru import logger
from telegram.ext import Application, CommandHandler

from src.admin.handlers import broadcasts, control, keywords, posts, rules, templates, welcome
from src.admin.handlers.common import start_handler, status_handler

if TYPE_CHECKING:
    from src.core.matcher import KeywordMatcher
    from src.database.repository import Repository
    from src.instagram.broadcast_manager import BroadcastManager
    from src.instagram.messenger import DirectMessenger
    from src.instagram.monitor import CommentMonitor


class AdminBot:
    """Telegram bot for administering InstaLeadMagnitBot."""

    def __init__(
        self,
        token: str,
        admin_ids: List[int],
        repository: "Repository",
    ):
        """Initialize admin bot.

        Args:
            token: Telegram bot token
            admin_ids: List of admin Telegram user IDs
            repository: Database repository
        """
        self.token = token
        self.admin_ids = admin_ids
        self.repository = repository
        self.application: Optional[Application] = None
        self._is_running = True

        # References to other components (set later)
        self._messenger: Optional["DirectMessenger"] = None
        self._monitor: Optional["CommentMonitor"] = None
        self._matcher: Optional["KeywordMatcher"] = None
        self._broadcast_manager: Optional["BroadcastManager"] = None

    def set_components(
        self,
        messenger: "DirectMessenger",
        monitor: "CommentMonitor",
        matcher: "KeywordMatcher",
        broadcast_manager: "BroadcastManager" = None,
    ) -> None:
        """Set references to other bot components.

        Args:
            messenger: Direct message sender
            monitor: Comment monitor
            matcher: Keyword matcher
            broadcast_manager: Broadcast manager
        """
        self._messenger = messenger
        self._monitor = monitor
        self._matcher = matcher
        self._broadcast_manager = broadcast_manager

    async def start(self) -> None:
        """Start the Telegram bot."""
        import asyncio

        try:
            self.application = Application.builder().token(self.token).build()

            # Store shared data in bot_data
            self.application.bot_data["repository"] = self.repository
            self.application.bot_data["admin_ids"] = self.admin_ids
            self.application.bot_data["messenger"] = self._messenger
            self.application.bot_data["monitor"] = self._monitor
            self.application.bot_data["matcher"] = self._matcher
            self.application.bot_data["broadcast_manager"] = self._broadcast_manager

            # Register handlers
            self._register_handlers()

            # Initialize and start
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling(drop_pending_updates=True)

            logger.info("Telegram admin bot started")

            # Keep running until stopped
            while self._is_running:
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")
            raise

    async def stop(self) -> None:
        """Stop the Telegram bot."""
        self._is_running = False
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            logger.info("Telegram admin bot stopped")

    def _register_handlers(self) -> None:
        """Register all command handlers."""
        app = self.application

        # Common commands
        app.add_handler(CommandHandler("start", start_handler))
        app.add_handler(CommandHandler("help", start_handler))
        app.add_handler(CommandHandler("status", status_handler))

        # Post commands
        app.add_handler(CommandHandler("posts", posts.list_posts))
        app.add_handler(CommandHandler("add_post", posts.add_post))
        app.add_handler(CommandHandler("remove_post", posts.remove_post))

        # Keyword commands
        app.add_handler(CommandHandler("keywords", keywords.list_keywords))
        app.add_handler(CommandHandler("add_keyword", keywords.add_keyword))
        app.add_handler(CommandHandler("remove_keyword", keywords.remove_keyword))

        # Template commands
        app.add_handler(CommandHandler("templates", templates.list_templates))
        app.add_handler(CommandHandler("add_template", templates.add_template))
        app.add_handler(CommandHandler("preview_template", templates.preview_template))

        # Rule commands
        app.add_handler(CommandHandler("rules", rules.list_rules))
        app.add_handler(CommandHandler("add_rule", rules.add_rule))
        app.add_handler(CommandHandler("toggle_rule", rules.toggle_rule))

        # Control commands
        app.add_handler(CommandHandler("pause", control.pause_bot))
        app.add_handler(CommandHandler("resume", control.resume_bot))

        # Welcome commands
        app.add_handler(CommandHandler("welcome", welcome.welcome_status))
        app.add_handler(CommandHandler("set_welcome", welcome.set_welcome))
        app.add_handler(CommandHandler("toggle_welcome", welcome.toggle_welcome))

        # Broadcast commands
        app.add_handler(CommandHandler("broadcasts", broadcasts.list_broadcasts))
        app.add_handler(CommandHandler("broadcast", broadcasts.create_broadcast))
        app.add_handler(CommandHandler("broadcast_status", broadcasts.broadcast_status))
        app.add_handler(CommandHandler("pause_broadcast", broadcasts.pause_broadcast))
        app.add_handler(CommandHandler("resume_broadcast", broadcasts.resume_broadcast))
        app.add_handler(CommandHandler("cancel_broadcast", broadcasts.cancel_broadcast))
        app.add_handler(CommandHandler("segments", broadcasts.list_segments))

        logger.debug("Telegram handlers registered")
