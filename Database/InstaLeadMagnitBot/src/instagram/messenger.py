"""Direct message sender with rate limiting."""

import asyncio
from collections import deque
from dataclasses import dataclass
from typing import TYPE_CHECKING

from loguru import logger

from src.utils.helpers import random_delay

if TYPE_CHECKING:
    from src.database.repository import Repository
    from .client import InstagramClient


@dataclass
class MessageTask:
    """Task for sending Direct message."""

    user_id: str
    username: str
    message: str
    post_id: int
    rule_id: int


class DirectMessenger:
    """Send Direct messages with rate limiting to avoid bans."""

    def __init__(
        self,
        client: "InstagramClient",
        repository: "Repository",
        delay_min: int = 30,
        delay_max: int = 60,
        max_per_hour: int = 50,
    ):
        """Initialize messenger.

        Args:
            client: Instagram API client
            repository: Database repository
            delay_min: Minimum delay between messages (seconds)
            delay_max: Maximum delay between messages (seconds)
            max_per_hour: Maximum messages per hour
        """
        self.client = client
        self.repository = repository
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.max_per_hour = max_per_hour

        self._queue: deque[MessageTask] = deque()
        self._is_running = False
        self._is_paused = False

    async def enqueue(self, task: MessageTask) -> None:
        """Add message task to queue.

        Args:
            task: Message task to enqueue
        """
        self._queue.append(task)
        logger.info(f"Message for {task.username} added to queue. Queue size: {len(self._queue)}")

    async def start(self) -> None:
        """Start message processing loop."""
        self._is_running = True
        logger.info("Direct messenger started")

        while self._is_running:
            if self._is_paused or not self._queue:
                await asyncio.sleep(1)
                continue

            # Check hourly limit
            sent_last_hour = await self.repository.get_messages_sent_last_hour()
            if sent_last_hour >= self.max_per_hour:
                logger.warning(
                    f"Hourly limit reached ({self.max_per_hour}), waiting..."
                )
                await asyncio.sleep(60)
                continue

            # Process next task
            task = self._queue.popleft()
            await self._send_message(task)

            # Random delay between messages
            if self._queue:  # Only delay if more messages pending
                await random_delay(self.delay_min, self.delay_max)

    def stop(self) -> None:
        """Stop message processing."""
        self._is_running = False
        logger.info("Direct messenger stopped")

    def pause(self) -> None:
        """Pause message sending."""
        self._is_paused = True
        logger.info("Direct messenger paused")

    def resume(self) -> None:
        """Resume message sending."""
        self._is_paused = False
        logger.info("Direct messenger resumed")

    async def _send_message(self, task: MessageTask) -> None:
        """Send single message.

        Args:
            task: Message task
        """
        try:
            success = await self.client.send_direct_message(task.user_id, task.message)

            status = "sent" if success else "failed"
            await self.repository.log_sent_message(
                user_id=task.user_id,
                username=task.username,
                post_id=task.post_id,
                rule_id=task.rule_id,
                status=status,
            )

            if success:
                logger.success(f"Message sent to {task.username}")
            else:
                logger.error(f"Failed to send message to {task.username}")

        except Exception as e:
            logger.error(f"Error sending message to {task.username}: {e}")
            await self.repository.log_sent_message(
                user_id=task.user_id,
                username=task.username,
                post_id=task.post_id,
                rule_id=task.rule_id,
                status="failed",
            )

    @property
    def queue_size(self) -> int:
        """Get current queue size."""
        return len(self._queue)

    @property
    def is_running(self) -> bool:
        """Check if messenger is running."""
        return self._is_running

    @property
    def is_paused(self) -> bool:
        """Check if messenger is paused."""
        return self._is_paused
