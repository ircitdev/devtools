"""Instagram API client wrapper using instagrapi."""

import asyncio
from functools import partial
from pathlib import Path
from typing import List, Optional

from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, LoginRequired
from instagrapi.types import Comment
from loguru import logger


class InstagramClient:
    """Wrapper around instagrapi with session management."""

    def __init__(self, username: str, password: str, session_file: Path):
        """Initialize Instagram client.

        Args:
            username: Instagram username
            password: Instagram password
            session_file: Path to save/load session
        """
        self.username = username
        self.password = password
        self.session_file = session_file
        self.client = Client()
        self.client.delay_range = [1, 3]  # Anti-spam delay between requests
        self._is_logged_in = False

    async def login(self) -> bool:
        """Login to Instagram with session reuse.

        Returns:
            True if login successful, False otherwise
        """
        try:
            # Try to load existing session
            if self.session_file.exists():
                logger.info("Loading saved session...")
                try:
                    self.client.load_settings(str(self.session_file))
                    self.client.login(self.username, self.password)

                    # Verify session is valid
                    await self._run_sync(self.client.get_timeline_feed)
                    logger.success("Session valid, logged in successfully")
                    self._is_logged_in = True
                    return True
                except Exception as e:
                    logger.warning(f"Session invalid: {e}, performing fresh login")

            # Fresh login
            logger.info("Performing fresh login...")
            await self._run_sync(partial(self.client.login, self.username, self.password))

            # Save session
            self.client.dump_settings(str(self.session_file))
            logger.success("Login successful, session saved")
            self._is_logged_in = True
            return True

        except ChallengeRequired as e:
            logger.error(f"Instagram verification required: {e}")
            logger.error("Please login manually in browser and complete verification")
            return False
        except LoginRequired as e:
            logger.error(f"Login required: {e}")
            return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    async def _run_sync(self, func, *args, **kwargs):
        """Run synchronous function in executor.

        Args:
            func: Synchronous function to run
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result
        """
        loop = asyncio.get_event_loop()
        if args or kwargs:
            func = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, func)

    async def get_media_pk_from_code(self, code: str) -> Optional[str]:
        """Get media PK from post shortcode.

        Args:
            code: Instagram post shortcode (e.g., 'ABC123' from url)

        Returns:
            Media PK as string or None if error
        """
        try:
            pk = await self._run_sync(partial(self.client.media_pk_from_code, code))
            return str(pk)
        except Exception as e:
            logger.error(f"Error getting media_pk for {code}: {e}")
            return None

    async def get_media_comments(self, media_pk: str, amount: int = 50) -> List[Comment]:
        """Get comments from media.

        Args:
            media_pk: Media PK (not shortcode)
            amount: Maximum number of comments to fetch

        Returns:
            List of Comment objects
        """
        try:
            comments = await self._run_sync(
                partial(self.client.media_comments, int(media_pk), amount)
            )
            return comments
        except Exception as e:
            logger.error(f"Error getting comments for {media_pk}: {e}")
            return []

    async def send_direct_message(self, user_id: str, text: str) -> bool:
        """Send Direct message to user.

        Args:
            user_id: Instagram user ID (pk)
            text: Message text

        Returns:
            True if sent successfully
        """
        try:
            await self._run_sync(partial(self.client.direct_send, text, [int(user_id)]))
            logger.info(f"Message sent to user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending message to {user_id}: {e}")
            return False

    async def get_user_info(self, user_id: str) -> Optional[dict]:
        """Get user info by ID.

        Args:
            user_id: Instagram user ID

        Returns:
            User info dict or None
        """
        try:
            user = await self._run_sync(partial(self.client.user_info, int(user_id)))
            return {
                "id": str(user.pk),
                "username": user.username,
                "full_name": user.full_name,
            }
        except Exception as e:
            logger.error(f"Error getting user info for {user_id}: {e}")
            return None

    @property
    def is_logged_in(self) -> bool:
        """Check if client is logged in."""
        return self._is_logged_in

    async def logout(self) -> None:
        """Logout from Instagram."""
        try:
            await self._run_sync(self.client.logout)
            self._is_logged_in = False
            logger.info("Logged out from Instagram")
        except Exception as e:
            logger.error(f"Error during logout: {e}")
