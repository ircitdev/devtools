"""Comment monitoring for Instagram posts."""

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Awaitable, Callable, Optional

from loguru import logger

if TYPE_CHECKING:
    from src.core.matcher import KeywordMatcher
    from src.database.repository import Repository
    from .client import InstagramClient


@dataclass
class CommentData:
    """Data structure for processed comment."""

    comment_id: str
    user_id: str
    username: str
    text: str
    post_instagram_id: str
    post_db_id: int


class CommentMonitor:
    """Monitor comments on Instagram posts for keywords."""

    def __init__(
        self,
        client: "InstagramClient",
        repository: "Repository",
        matcher: "KeywordMatcher",
        check_interval: int = 60,
    ):
        """Initialize comment monitor.

        Args:
            client: Instagram API client
            repository: Database repository
            matcher: Keyword matcher
            check_interval: Seconds between comment checks
        """
        self.client = client
        self.repository = repository
        self.matcher = matcher
        self.check_interval = check_interval
        self._is_running = False
        self._is_paused = False
        self._on_match_callback: Optional[Callable[[CommentData, int], Awaitable[None]]] = None
        # Cache for media PKs (shortcode -> pk)
        self._media_pk_cache: dict[str, str] = {}

    def set_match_callback(
        self, callback: Callable[[CommentData, int], Awaitable[None]]
    ) -> None:
        """Set callback for when keyword match is found.

        Args:
            callback: Async function(comment_data, rule_id)
        """
        self._on_match_callback = callback

    async def start(self) -> None:
        """Start monitoring loop."""
        self._is_running = True
        logger.info("Comment monitoring started")

        while self._is_running:
            if not self._is_paused:
                try:
                    await self._check_all_posts()
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")

            await asyncio.sleep(self.check_interval)

    def stop(self) -> None:
        """Stop monitoring loop."""
        self._is_running = False
        logger.info("Comment monitoring stopped")

    def pause(self) -> None:
        """Pause monitoring."""
        self._is_paused = True
        logger.info("Comment monitoring paused")

    def resume(self) -> None:
        """Resume monitoring."""
        self._is_paused = False
        logger.info("Comment monitoring resumed")

    async def _check_all_posts(self) -> None:
        """Check comments on all active posts."""
        posts = await self.repository.get_active_posts()

        if not posts:
            logger.debug("No active posts to monitor")
            return

        for post in posts:
            await self._check_post_comments(post)

    async def _get_media_pk(self, instagram_id: str) -> Optional[str]:
        """Get media PK with caching.

        Args:
            instagram_id: Post shortcode

        Returns:
            Media PK or None
        """
        if instagram_id in self._media_pk_cache:
            return self._media_pk_cache[instagram_id]

        pk = await self.client.get_media_pk_from_code(instagram_id)
        if pk:
            self._media_pk_cache[instagram_id] = pk
        return pk

    async def _check_post_comments(self, post) -> None:
        """Check comments on single post.

        Args:
            post: Post database model
        """
        logger.debug(f"Checking comments for post {post.instagram_id}")

        # Get media PK from shortcode
        media_pk = await self._get_media_pk(post.instagram_id)
        if not media_pk:
            logger.warning(f"Could not get media_pk for {post.instagram_id}")
            return

        comments = await self.client.get_media_comments(media_pk, amount=50)

        for comment in comments:
            comment_id = str(comment.pk)

            # Skip already processed comments
            if await self.repository.is_comment_processed(comment_id):
                continue

            # Find matching keyword rule
            matched_rule = await self.matcher.find_matching_rule(
                text=comment.text, post_id=post.id
            )

            if matched_rule:
                user_id = str(comment.user.pk)

                # Check if user already received message for this post
                if await self.repository.has_user_received_message(user_id, post.id):
                    logger.debug(
                        f"User {user_id} already received message for post {post.id}"
                    )
                    await self.repository.mark_comment_processed(comment_id)
                    continue

                # Trigger callback for message sending
                if self._on_match_callback:
                    comment_data = CommentData(
                        comment_id=comment_id,
                        user_id=user_id,
                        username=comment.user.username,
                        text=comment.text,
                        post_instagram_id=post.instagram_id,
                        post_db_id=post.id,
                    )
                    await self._on_match_callback(comment_data, matched_rule.id)

            # Mark comment as processed
            await self.repository.mark_comment_processed(comment_id)

    @property
    def is_running(self) -> bool:
        """Check if monitor is running."""
        return self._is_running

    @property
    def is_paused(self) -> bool:
        """Check if monitor is paused."""
        return self._is_paused
