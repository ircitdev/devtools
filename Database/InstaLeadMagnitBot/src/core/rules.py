"""Rules engine for processing keyword matches."""

from typing import TYPE_CHECKING

from loguru import logger

from src.instagram.messenger import MessageTask
from src.utils.helpers import format_template

if TYPE_CHECKING:
    from src.database.repository import Repository
    from src.instagram.messenger import DirectMessenger
    from src.instagram.monitor import CommentData
    from .matcher import KeywordMatcher


class RulesEngine:
    """Process keyword matches and trigger message sending."""

    def __init__(
        self,
        repository: "Repository",
        matcher: "KeywordMatcher",
        messenger: "DirectMessenger",
    ):
        """Initialize rules engine.

        Args:
            repository: Database repository
            matcher: Keyword matcher
            messenger: Direct message sender
        """
        self.repository = repository
        self.matcher = matcher
        self.messenger = messenger

    async def process_match(self, comment: "CommentData", rule_id: int) -> None:
        """Process keyword match and enqueue message.

        Args:
            comment: Comment data
            rule_id: ID of matched rule
        """
        # Get rule with template
        rules = await self.repository.get_active_rules()
        rule = next((r for r in rules if r.id == rule_id), None)

        if not rule or not rule.template:
            logger.warning(f"Rule {rule_id} not found or has no template")
            return

        # Format message with variables
        message = format_template(
            rule.template.content,
            username=comment.username,
            post_url=f"https://instagram.com/p/{comment.post_instagram_id}",
            keyword=rule.keyword.word if rule.keyword else "",
        )

        # Create message task
        task = MessageTask(
            user_id=comment.user_id,
            username=comment.username,
            message=message,
            post_id=comment.post_db_id,
            rule_id=rule_id,
        )

        await self.messenger.enqueue(task)
        logger.info(f"Message task created for {comment.username} (rule {rule_id})")
