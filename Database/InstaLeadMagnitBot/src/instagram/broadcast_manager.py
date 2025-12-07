"""Broadcast manager for mass DM campaigns."""

import asyncio
import random
from datetime import datetime
from typing import TYPE_CHECKING, Callable, Optional

from loguru import logger

if TYPE_CHECKING:
    from src.database.repository import Repository
    from src.instagram.client import InstagramClient
    from src.utils.sheets_logger import GoogleSheetsLogger


class BroadcastManager:
    """Manages mass broadcast campaigns with rate limiting."""

    def __init__(
        self,
        client: "InstagramClient",
        repository: "Repository",
        delay_min: int = 45,
        delay_max: int = 90,
        max_per_hour: int = 30,
        sheets_logger: Optional["GoogleSheetsLogger"] = None,
    ):
        """Initialize broadcast manager.

        Args:
            client: Instagram client
            repository: Database repository
            delay_min: Minimum delay between messages (seconds)
            delay_max: Maximum delay between messages (seconds)
            max_per_hour: Maximum messages per hour (for rate limiting)
            sheets_logger: Optional Google Sheets logger
        """
        self.client = client
        self.repository = repository
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.max_per_hour = max_per_hour
        self.sheets_logger = sheets_logger

        self._running = False
        self._current_broadcast_id: Optional[int] = None
        self._messages_sent_this_hour = 0
        self._hour_start = datetime.utcnow()
        self._status_callback: Optional[Callable] = None

    def set_status_callback(self, callback: Callable) -> None:
        """Set callback for status updates.

        Args:
            callback: Async function(broadcast_id, sent, failed, total, status)
        """
        self._status_callback = callback

    async def start(self) -> None:
        """Start the broadcast manager background task."""
        self._running = True
        logger.info("Broadcast manager started")

        while self._running:
            try:
                # Check for active broadcasts
                broadcasts = await self.repository.get_active_broadcasts()

                for broadcast in broadcasts:
                    if not self._running:
                        break
                    await self._process_broadcast(broadcast.id)

                # Sleep before next check
                await asyncio.sleep(5)

            except Exception as e:
                logger.error(f"Broadcast manager error: {e}")
                await asyncio.sleep(10)

    def stop(self) -> None:
        """Stop the broadcast manager."""
        self._running = False
        logger.info("Broadcast manager stopped")

    async def _process_broadcast(self, broadcast_id: int) -> None:
        """Process a single broadcast campaign.

        Args:
            broadcast_id: ID of broadcast to process
        """
        self._current_broadcast_id = broadcast_id
        broadcast = await self.repository.get_broadcast(broadcast_id)

        if not broadcast:
            return

        # Check rate limit
        await self._check_rate_limit()

        # Get pending recipients
        recipients = await self.repository.get_pending_recipients(broadcast_id, limit=5)

        if not recipients:
            # No more pending - mark as completed
            await self.repository.update_broadcast_status(broadcast_id, "completed")
            logger.info(f"Broadcast {broadcast_id} completed")

            if self.sheets_logger:
                await self.sheets_logger.log_broadcast(
                    broadcast_id=broadcast_id,
                    segment=broadcast.segment_type.value,
                    total_users=broadcast.total_users,
                    sent=broadcast.sent_count,
                    failed=broadcast.failed_count,
                    status="completed",
                )
            return

        # Send messages to recipients
        for recipient in recipients:
            if not self._running:
                break

            await self._check_rate_limit()

            success = await self._send_broadcast_message(
                broadcast.message,
                recipient.instagram_user_id,
                recipient.username,
            )

            if success:
                await self.repository.update_recipient_status(recipient.id, "sent")
                await self.repository.increment_broadcast_counts(broadcast_id, sent=1)
                self._messages_sent_this_hour += 1

                if self.sheets_logger:
                    await self.sheets_logger.log_sent_message(
                        username=recipient.username,
                        user_id=recipient.instagram_user_id,
                        post_id=0,
                        rule_id=0,
                        status="sent",
                        message_preview=f"[BROADCAST {broadcast_id}] {broadcast.message[:50]}",
                    )
            else:
                await self.repository.update_recipient_status(
                    recipient.id, "failed", "Send failed"
                )
                await self.repository.increment_broadcast_counts(broadcast_id, failed=1)

            # Notify status
            if self._status_callback:
                updated = await self.repository.get_broadcast(broadcast_id)
                if updated:
                    await self._status_callback(
                        broadcast_id,
                        updated.sent_count,
                        updated.failed_count,
                        updated.total_users,
                        "in_progress",
                    )

            # Random delay between messages
            delay = random.randint(self.delay_min, self.delay_max)
            logger.debug(f"Broadcast delay: {delay}s")
            await asyncio.sleep(delay)

    async def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        now = datetime.utcnow()

        # Reset counter every hour
        if (now - self._hour_start).total_seconds() >= 3600:
            self._messages_sent_this_hour = 0
            self._hour_start = now
            logger.debug("Broadcast rate limit reset")

        # If at limit, wait
        if self._messages_sent_this_hour >= self.max_per_hour:
            wait_seconds = 3600 - (now - self._hour_start).total_seconds()
            if wait_seconds > 0:
                logger.warning(f"Broadcast rate limit reached, waiting {wait_seconds:.0f}s")
                await asyncio.sleep(wait_seconds)
                self._messages_sent_this_hour = 0
                self._hour_start = datetime.utcnow()

    async def _send_broadcast_message(
        self, message: str, user_id: str, username: str
    ) -> bool:
        """Send a broadcast message to a user.

        Args:
            message: Message text (can contain {username})
            user_id: Instagram user ID
            username: Instagram username

        Returns:
            True if sent successfully
        """
        try:
            # Format message with username
            formatted = message.replace("{username}", username)

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.client.client.direct_send(formatted, user_ids=[int(user_id)]),
            )

            if result:
                logger.info(f"Broadcast message sent to {username}")
                return True
            return False

        except Exception as e:
            logger.error(f"Failed to send broadcast to {username}: {e}")
            if self.sheets_logger:
                await self.sheets_logger.log_error(
                    component="broadcast_manager",
                    error_type="send_failed",
                    message=f"Failed to send to {username}",
                    details=str(e),
                )
            return False

    async def create_and_start_broadcast(
        self,
        name: str,
        message: str,
        segment_type: str,
        segment_filter: Optional[str] = None,
    ) -> Optional[int]:
        """Create a new broadcast and start it.

        Args:
            name: Broadcast name
            message: Message text
            segment_type: Type of user segment
            segment_filter: Filter value (keyword_id or days)

        Returns:
            Broadcast ID if created successfully
        """
        try:
            # Create broadcast
            broadcast = await self.repository.create_broadcast(
                name=name,
                message=message,
                segment_type=segment_type,
                segment_filter=segment_filter,
            )

            # Get users based on segment
            users = await self._get_segment_users(segment_type, segment_filter)

            if not users:
                logger.warning(f"No users found for segment {segment_type}")
                await self.repository.delete_broadcast(broadcast.id)
                return None

            # Add recipients
            await self.repository.add_broadcast_recipients(broadcast.id, users)

            # Start broadcast
            await self.repository.update_broadcast_status(broadcast.id, "in_progress")

            if self.sheets_logger:
                await self.sheets_logger.log_broadcast(
                    broadcast_id=broadcast.id,
                    segment=segment_type,
                    total_users=len(users),
                    sent=0,
                    failed=0,
                    status="started",
                )

            logger.info(f"Broadcast {broadcast.id} created with {len(users)} recipients")
            return broadcast.id

        except Exception as e:
            logger.error(f"Failed to create broadcast: {e}")
            return None

    async def _get_segment_users(
        self, segment_type: str, segment_filter: Optional[str]
    ) -> list:
        """Get users for a segment.

        Args:
            segment_type: Type of segment
            segment_filter: Filter value

        Returns:
            List of user dicts
        """
        if segment_type == "keyword_commenters":
            if not segment_filter:
                return []
            return await self.repository.get_users_by_keyword(int(segment_filter))

        elif segment_type == "new_followers":
            days = int(segment_filter) if segment_filter else 7
            return await self.repository.get_recent_followers(days)

        elif segment_type == "all_commenters":
            return await self.repository.get_all_commenters()

        return []

    async def pause_broadcast(self, broadcast_id: int) -> bool:
        """Pause a broadcast.

        Args:
            broadcast_id: Broadcast ID

        Returns:
            True if paused
        """
        broadcast = await self.repository.update_broadcast_status(broadcast_id, "paused")
        if broadcast:
            logger.info(f"Broadcast {broadcast_id} paused")
            return True
        return False

    async def resume_broadcast(self, broadcast_id: int) -> bool:
        """Resume a paused broadcast.

        Args:
            broadcast_id: Broadcast ID

        Returns:
            True if resumed
        """
        broadcast = await self.repository.update_broadcast_status(broadcast_id, "in_progress")
        if broadcast:
            logger.info(f"Broadcast {broadcast_id} resumed")
            return True
        return False

    async def cancel_broadcast(self, broadcast_id: int) -> bool:
        """Cancel a broadcast.

        Args:
            broadcast_id: Broadcast ID

        Returns:
            True if cancelled
        """
        broadcast = await self.repository.update_broadcast_status(broadcast_id, "cancelled")
        if broadcast:
            logger.info(f"Broadcast {broadcast_id} cancelled")
            return True
        return False
