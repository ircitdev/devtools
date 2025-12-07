"""Keyword matching engine."""

import re
from typing import TYPE_CHECKING, List, Optional

from loguru import logger

from src.database.models import MatchType, Rule

if TYPE_CHECKING:
    from src.database.repository import Repository


class KeywordMatcher:
    """Match comment text against keywords."""

    def __init__(self, repository: "Repository"):
        """Initialize keyword matcher.

        Args:
            repository: Database repository
        """
        self.repository = repository
        self._rules_cache: List[Rule] = []
        self._cache_valid = False

    async def refresh_cache(self) -> None:
        """Refresh rules cache from database."""
        self._rules_cache = await self.repository.get_active_rules()
        self._cache_valid = True
        logger.debug(f"Rules cache refreshed: {len(self._rules_cache)} active rules")

    def invalidate_cache(self) -> None:
        """Invalidate rules cache."""
        self._cache_valid = False
        logger.debug("Rules cache invalidated")

    async def find_matching_rule(self, text: str, post_id: int) -> Optional[Rule]:
        """Find first rule matching the text for given post.

        Args:
            text: Comment text to match
            post_id: Database ID of post

        Returns:
            Matching Rule or None
        """
        if not self._cache_valid:
            await self.refresh_cache()

        text_lower = text.lower()

        for rule in self._rules_cache:
            # Check post binding (None means global rule)
            if rule.post_id is not None and rule.post_id != post_id:
                continue

            keyword = rule.keyword
            if not keyword or not keyword.is_active:
                continue

            # Check keyword match
            if self._matches(text_lower, keyword.word, keyword.match_type):
                logger.info(f"Keyword match: '{keyword.word}' in text")
                return rule

        return None

    def _matches(self, text: str, keyword: str, match_type: MatchType) -> bool:
        """Check if text matches keyword according to match type.

        Args:
            text: Lowercase text to search in
            keyword: Keyword to find
            match_type: Type of matching

        Returns:
            True if matches
        """
        keyword_lower = keyword.lower()

        if match_type == MatchType.EXACT:
            # Exact word match (word boundaries)
            words = re.findall(r"\w+", text, re.UNICODE)
            return keyword_lower in [w.lower() for w in words]

        elif match_type == MatchType.CONTAINS:
            # Substring match
            return keyword_lower in text

        elif match_type == MatchType.REGEX:
            # Regular expression match
            try:
                return bool(re.search(keyword, text, re.IGNORECASE))
            except re.error as e:
                logger.warning(f"Invalid regex pattern '{keyword}': {e}")
                return False

        return False
