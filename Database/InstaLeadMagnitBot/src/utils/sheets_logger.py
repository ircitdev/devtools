"""Google Sheets logger for event tracking."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials
from loguru import logger


class GoogleSheetsLogger:
    """Logger that writes events to Google Sheets with multiple tabs."""

    # Sheet names (tabs)
    TAB_EVENTS = "Events"
    TAB_SENT_MESSAGES = "SentMessages"
    TAB_NEW_FOLLOWERS = "NewFollowers"
    TAB_COMMENTS = "Comments"
    TAB_ERRORS = "Errors"
    TAB_BROADCASTS = "Broadcasts"

    def __init__(
        self,
        credentials_file: str,
        spreadsheet_id: str,
    ):
        """Initialize Google Sheets logger.

        Args:
            credentials_file: Path to service account JSON file
            spreadsheet_id: Google Spreadsheet ID
        """
        self.credentials_file = Path(credentials_file)
        self.spreadsheet_id = spreadsheet_id
        self._client: Optional[gspread.Client] = None
        self._spreadsheet: Optional[gspread.Spreadsheet] = None
        self._sheets: dict = {}
        self._initialized = False
        self._queue = asyncio.Queue()
        self._running = False

    async def initialize(self) -> bool:
        """Initialize connection to Google Sheets.

        Returns:
            True if initialization successful
        """
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._connect)
            self._initialized = True
            logger.info("Google Sheets logger initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets: {e}")
            return False

    def _connect(self) -> None:
        """Connect to Google Sheets (sync)."""
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_file(
            str(self.credentials_file), scopes=scopes
        )
        self._client = gspread.authorize(credentials)
        self._spreadsheet = self._client.open_by_key(self.spreadsheet_id)

        # Get or create sheets
        self._ensure_sheets()

    def _ensure_sheets(self) -> None:
        """Ensure all required sheets exist with headers."""
        existing = [ws.title for ws in self._spreadsheet.worksheets()]

        # Define headers for each sheet
        headers = {
            self.TAB_EVENTS: ["Timestamp", "Type", "Description", "Details"],
            self.TAB_SENT_MESSAGES: [
                "Timestamp",
                "Username",
                "User ID",
                "Post ID",
                "Rule ID",
                "Status",
                "Message Preview",
            ],
            self.TAB_NEW_FOLLOWERS: [
                "Timestamp",
                "Username",
                "User ID",
                "Welcome Sent",
                "Message Preview",
            ],
            self.TAB_COMMENTS: [
                "Timestamp",
                "Post ID",
                "Username",
                "User ID",
                "Comment Text",
                "Matched Keyword",
                "Action Taken",
            ],
            self.TAB_ERRORS: ["Timestamp", "Component", "Error Type", "Message", "Details"],
            self.TAB_BROADCASTS: [
                "Timestamp",
                "Broadcast ID",
                "Segment",
                "Total Users",
                "Sent",
                "Failed",
                "Status",
            ],
        }

        for tab_name, tab_headers in headers.items():
            if tab_name not in existing:
                # Create new sheet
                worksheet = self._spreadsheet.add_worksheet(
                    title=tab_name, rows=1000, cols=len(tab_headers)
                )
                worksheet.append_row(tab_headers)
                logger.info(f"Created sheet: {tab_name}")
            else:
                worksheet = self._spreadsheet.worksheet(tab_name)

            self._sheets[tab_name] = worksheet

    async def start(self) -> None:
        """Start the async queue processor."""
        self._running = True
        logger.info("Google Sheets logger queue started")

        while self._running:
            try:
                # Wait for items in queue
                item = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                sheet_name, row_data = item

                # Write to sheet
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None, self._write_row, sheet_name, row_data
                )
                self._queue.task_done()

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing sheets queue: {e}")

    def stop(self) -> None:
        """Stop the queue processor."""
        self._running = False
        logger.info("Google Sheets logger stopped")

    def _write_row(self, sheet_name: str, row_data: list) -> None:
        """Write a row to specified sheet (sync)."""
        try:
            if sheet_name in self._sheets:
                self._sheets[sheet_name].append_row(row_data)
        except Exception as e:
            logger.error(f"Failed to write to sheet {sheet_name}: {e}")

    def _timestamp(self) -> str:
        """Get current timestamp string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # === Event Logging Methods ===

    async def log_event(self, event_type: str, description: str, details: str = "") -> None:
        """Log a general event.

        Args:
            event_type: Type of event (startup, shutdown, config_change, etc.)
            description: Short description
            details: Additional details
        """
        if not self._initialized:
            return
        await self._queue.put(
            (self.TAB_EVENTS, [self._timestamp(), event_type, description, details])
        )

    async def log_sent_message(
        self,
        username: str,
        user_id: str,
        post_id: int,
        rule_id: int,
        status: str,
        message_preview: str = "",
    ) -> None:
        """Log a sent direct message.

        Args:
            username: Instagram username
            user_id: Instagram user ID
            post_id: Post database ID
            rule_id: Rule database ID
            status: Message status (sent, failed, pending)
            message_preview: First 100 chars of message
        """
        if not self._initialized:
            return
        await self._queue.put(
            (
                self.TAB_SENT_MESSAGES,
                [
                    self._timestamp(),
                    username,
                    user_id,
                    str(post_id),
                    str(rule_id),
                    status,
                    message_preview[:100] if message_preview else "",
                ],
            )
        )

    async def log_new_follower(
        self,
        username: str,
        user_id: str,
        welcome_sent: bool,
        message_preview: str = "",
    ) -> None:
        """Log a new follower.

        Args:
            username: Instagram username
            user_id: Instagram user ID
            welcome_sent: Whether welcome message was sent
            message_preview: First 100 chars of welcome message
        """
        if not self._initialized:
            return
        await self._queue.put(
            (
                self.TAB_NEW_FOLLOWERS,
                [
                    self._timestamp(),
                    username,
                    user_id,
                    "Yes" if welcome_sent else "No",
                    message_preview[:100] if message_preview else "",
                ],
            )
        )

    async def log_comment(
        self,
        post_id: str,
        username: str,
        user_id: str,
        comment_text: str,
        matched_keyword: str = "",
        action_taken: str = "",
    ) -> None:
        """Log a processed comment.

        Args:
            post_id: Instagram post ID
            username: Comment author username
            user_id: Comment author user ID
            comment_text: Comment text
            matched_keyword: Keyword that was matched (if any)
            action_taken: What action was taken (dm_sent, dm_queued, ignored)
        """
        if not self._initialized:
            return
        await self._queue.put(
            (
                self.TAB_COMMENTS,
                [
                    self._timestamp(),
                    post_id,
                    username,
                    user_id,
                    comment_text[:200] if comment_text else "",
                    matched_keyword,
                    action_taken,
                ],
            )
        )

    async def log_error(
        self,
        component: str,
        error_type: str,
        message: str,
        details: str = "",
    ) -> None:
        """Log an error.

        Args:
            component: Component name (monitor, messenger, admin_bot, etc.)
            error_type: Type of error
            message: Error message
            details: Additional details or stack trace
        """
        if not self._initialized:
            return
        await self._queue.put(
            (
                self.TAB_ERRORS,
                [
                    self._timestamp(),
                    component,
                    error_type,
                    message,
                    details[:500] if details else "",
                ],
            )
        )

    async def log_broadcast(
        self,
        broadcast_id: int,
        segment: str,
        total_users: int,
        sent: int,
        failed: int,
        status: str,
    ) -> None:
        """Log a broadcast operation.

        Args:
            broadcast_id: Broadcast database ID
            segment: User segment name
            total_users: Total users in segment
            sent: Number of messages sent
            failed: Number of failed sends
            status: Broadcast status (in_progress, completed, paused, cancelled)
        """
        if not self._initialized:
            return
        await self._queue.put(
            (
                self.TAB_BROADCASTS,
                [
                    self._timestamp(),
                    str(broadcast_id),
                    segment,
                    str(total_users),
                    str(sent),
                    str(failed),
                    status,
                ],
            )
        )
