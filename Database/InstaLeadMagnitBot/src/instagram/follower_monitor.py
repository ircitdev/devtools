"""Monitor for new Instagram followers and send welcome messages."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Optional, Set

from loguru import logger

if TYPE_CHECKING:
    from src.database.repository import Repository
    from src.instagram.client import InstagramClient


class FollowerMonitor:
    """Monitor new followers and send welcome messages."""

    def __init__(
        self,
        client: "InstagramClient",
        repository: "Repository",
        check_interval: int = 300,
    ):
        """Initialize follower monitor.

        Args:
            client: Instagram client
            repository: Database repository
            check_interval: Interval between checks in seconds (default 5 min)
        """
        self.client = client
        self.repository = repository
        self.check_interval = check_interval
        self._is_running = False
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._known_followers: Set[str] = set()
        self._initialized = False

    async def start(self) -> None:
        """Start monitoring followers."""
        self._is_running = True
        logger.info("Follower monitoring started")

        # Initialize known followers on first run
        if not self._initialized:
            await self._initialize_known_followers()
            self._initialized = True

        while self._is_running:
            try:
                await self._check_new_followers()
            except Exception as e:
                logger.error(f"Error checking followers: {e}")

            await asyncio.sleep(self.check_interval)

    def stop(self) -> None:
        """Stop monitoring."""
        self._is_running = False
        logger.info("Follower monitoring stopped")

    async def _initialize_known_followers(self) -> None:
        """Load current followers to avoid welcoming existing ones."""
        try:
            loop = asyncio.get_event_loop()
            followers = await loop.run_in_executor(
                self._executor,
                self._get_followers_sync
            )
            self._known_followers = {str(f.pk) for f in followers}
            logger.info(f"Initialized with {len(self._known_followers)} existing followers")
        except Exception as e:
            logger.error(f"Error initializing followers: {e}")

    def _get_followers_sync(self):
        """Get followers synchronously (for executor)."""
        user_id = self.client.client.user_id
        return self.client.client.user_followers(user_id, amount=0)

    async def _check_new_followers(self) -> None:
        """Check for new followers and send welcome messages."""
        settings = await self.repository.get_welcome_settings()
        if not settings or not settings.is_enabled or not settings.message:
            return

        try:
            loop = asyncio.get_event_loop()
            current_followers = await loop.run_in_executor(
                self._executor,
                self._get_followers_sync
            )
            current_ids = {str(f.pk) for f in current_followers}

            # Find new followers
            new_follower_ids = current_ids - self._known_followers

            if new_follower_ids:
                logger.info(f"Found {len(new_follower_ids)} new followers")

                for follower in current_followers:
                    follower_id = str(follower.pk)
                    if follower_id in new_follower_ids:
                        # Check if already welcomed
                        if await self.repository.is_follower_welcomed(follower_id):
                            continue

                        # Send welcome message
                        await self._send_welcome(follower_id, follower.username, settings.message)

            # Update known followers
            self._known_followers = current_ids

        except Exception as e:
            logger.error(f"Error in follower check: {e}")

    async def _send_welcome(self, user_id: str, username: str, message: str) -> None:
        """Send welcome message to new follower."""
        try:
            # Format message with username
            formatted_message = message.replace("{username}", username)

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                self._executor,
                lambda: self.client.client.direct_send(formatted_message, user_ids=[int(user_id)])
            )

            # Mark as welcomed
            await self.repository.mark_follower_welcomed(user_id, username)
            logger.success(f"Welcome message sent to @{username}")

            # Rate limiting delay
            await asyncio.sleep(30)

        except Exception as e:
            logger.error(f"Failed to send welcome to @{username}: {e}")
