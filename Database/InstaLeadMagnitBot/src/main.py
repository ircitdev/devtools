"""Main entry point for InstaLeadMagnitBot."""

import asyncio
import sys
from pathlib import Path

from loguru import logger

from src.admin.bot import AdminBot
from src.config import get_settings
from src.core.matcher import KeywordMatcher
from src.core.rules import RulesEngine
from src.database.repository import Repository
from src.instagram.broadcast_manager import BroadcastManager
from src.instagram.client import InstagramClient
from src.instagram.messenger import DirectMessenger
from src.instagram.monitor import CommentMonitor
from src.instagram.follower_monitor import FollowerMonitor
from src.utils.helpers import setup_logging
from src.utils.sheets_logger import GoogleSheetsLogger


class Application:
    """Main application class coordinating all components."""

    def __init__(self):
        """Initialize application."""
        self.settings = get_settings()
        self.repository: Repository = None
        self.instagram_client: InstagramClient = None
        self.monitor: CommentMonitor = None
        self.messenger: DirectMessenger = None
        self.matcher: KeywordMatcher = None
        self.rules_engine: RulesEngine = None
        self.admin_bot: AdminBot = None
        self.follower_monitor: FollowerMonitor = None
        self.broadcast_manager: BroadcastManager = None
        self.sheets_logger: GoogleSheetsLogger = None
        self._shutdown_event = asyncio.Event()
        self._tasks = []

    async def initialize(self) -> bool:
        """Initialize all components.

        Returns:
            True if initialization successful
        """
        logger.info("Initializing application...")

        # Create directories
        Path("data").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)

        # Setup logging
        setup_logging(self.settings.log_level, str(self.settings.log_file_path))

        # Initialize database
        self.repository = Repository(self.settings.database_url)
        await self.repository.init_db()
        logger.info("Database initialized")

        # Initialize Instagram client
        self.instagram_client = InstagramClient(
            username=self.settings.instagram_username,
            password=self.settings.instagram_password,
            session_file=self.settings.session_file_path,
        )

        if not await self.instagram_client.login():
            logger.error("Failed to login to Instagram")
            return False

        # Initialize business logic components
        self.matcher = KeywordMatcher(self.repository)

        self.messenger = DirectMessenger(
            client=self.instagram_client,
            repository=self.repository,
            delay_min=self.settings.message_delay_min_seconds,
            delay_max=self.settings.message_delay_max_seconds,
            max_per_hour=self.settings.max_messages_per_hour,
        )

        self.rules_engine = RulesEngine(
            repository=self.repository,
            matcher=self.matcher,
            messenger=self.messenger,
        )

        self.monitor = CommentMonitor(
            client=self.instagram_client,
            repository=self.repository,
            matcher=self.matcher,
            check_interval=self.settings.check_interval_seconds,
        )
        self.monitor.set_match_callback(self.rules_engine.process_match)

        # Initialize follower monitor for welcome messages
        self.follower_monitor = FollowerMonitor(
            client=self.instagram_client,
            repository=self.repository,
            check_interval=300,  # Check every 5 minutes
        )

        # Initialize Google Sheets logger
        if self.settings.google_sheets_enabled and self.settings.google_spreadsheet_id:
            self.sheets_logger = GoogleSheetsLogger(
                credentials_file=self.settings.google_credentials_file,
                spreadsheet_id=self.settings.google_spreadsheet_id,
            )
            if await self.sheets_logger.initialize():
                logger.info("Google Sheets logger initialized")
            else:
                logger.warning("Google Sheets logger failed to initialize, continuing without it")
                self.sheets_logger = None

        # Initialize broadcast manager
        self.broadcast_manager = BroadcastManager(
            client=self.instagram_client,
            repository=self.repository,
            delay_min=45,
            delay_max=90,
            max_per_hour=30,
            sheets_logger=self.sheets_logger,
        )

        # Initialize Telegram bot
        self.admin_bot = AdminBot(
            token=self.settings.telegram_bot_token,
            admin_ids=self.settings.admin_ids_list,
            repository=self.repository,
        )
        self.admin_bot.set_components(
            messenger=self.messenger,
            monitor=self.monitor,
            matcher=self.matcher,
            broadcast_manager=self.broadcast_manager,
        )

        # Log startup event
        if self.sheets_logger:
            await self.sheets_logger.log_event("startup", "Bot started", "All components initialized")

        logger.success("Application initialized successfully")
        return True

    async def run(self) -> None:
        """Run all components."""
        logger.info("Starting components...")

        # Create tasks for all components
        self._tasks = [
            asyncio.create_task(self.monitor.start(), name="monitor"),
            asyncio.create_task(self.messenger.start(), name="messenger"),
            asyncio.create_task(self.admin_bot.start(), name="admin_bot"),
            asyncio.create_task(self.follower_monitor.start(), name="follower_monitor"),
            asyncio.create_task(self.broadcast_manager.start(), name="broadcast_manager"),
        ]

        # Add sheets logger task if enabled
        if self.sheets_logger:
            self._tasks.append(
                asyncio.create_task(self.sheets_logger.start(), name="sheets_logger")
            )

        logger.success("All components started")
        logger.info("Bot is running. Press Ctrl+C to stop.")

        # Wait for shutdown signal
        await self._shutdown_event.wait()

        # Cancel all tasks
        for task in self._tasks:
            task.cancel()

        await asyncio.gather(*self._tasks, return_exceptions=True)

    async def shutdown(self) -> None:
        """Graceful shutdown."""
        logger.info("Shutting down application...")

        # Log shutdown
        if self.sheets_logger:
            await self.sheets_logger.log_event("shutdown", "Bot shutting down", "Graceful shutdown initiated")

        # Stop components
        if self.monitor:
            self.monitor.stop()
        if self.messenger:
            self.messenger.stop()
        if self.admin_bot:
            await self.admin_bot.stop()
        if self.follower_monitor:
            self.follower_monitor.stop()
        if self.broadcast_manager:
            self.broadcast_manager.stop()
        if self.sheets_logger:
            self.sheets_logger.stop()

        self._shutdown_event.set()
        logger.info("Application stopped")


async def main():
    """Main entry point."""
    app = Application()

    # Handle shutdown signals
    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(app.shutdown())

    # Setup signal handlers (Unix only)
    if sys.platform != "win32":
        import signal

        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, signal_handler)

    try:
        if await app.initialize():
            await app.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
        await app.shutdown()
    except Exception as e:
        logger.exception(f"Critical error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
