"""Database repository for CRUD operations."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from .models import (
    Base,
    Broadcast,
    BroadcastRecipient,
    BroadcastStatus,
    Keyword,
    MatchType,
    MessageStatus,
    MessageTemplate,
    Post,
    ProcessedComment,
    ProcessedFollower,
    Rule,
    SegmentType,
    SentMessage,
    WelcomeSettings,
)


class Repository:
    """Repository for database operations."""

    def __init__(self, database_url: str):
        """Initialize repository with database URL.

        Args:
            database_url: SQLAlchemy async database URL
        """
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def init_db(self) -> None:
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

    # === Posts ===

    async def get_all_posts(self) -> List[Post]:
        """Get all posts."""
        async with self.async_session() as session:
            result = await session.execute(select(Post).order_by(Post.created_at.desc()))
            return list(result.scalars().all())

    async def get_active_posts(self) -> List[Post]:
        """Get all active posts for monitoring."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Post).where(Post.is_active == True).order_by(Post.created_at.desc())
            )
            return list(result.scalars().all())

    async def add_post(self, instagram_id: str, url: str) -> Post:
        """Add new post to monitoring."""
        async with self.async_session() as session:
            post = Post(instagram_id=instagram_id, url=url)
            session.add(post)
            await session.commit()
            await session.refresh(post)
            logger.info(f"Post added: {instagram_id}")
            return post

    async def get_post_by_instagram_id(self, instagram_id: str) -> Optional[Post]:
        """Get post by Instagram shortcode."""
        async with self.async_session() as session:
            result = await session.execute(select(Post).where(Post.instagram_id == instagram_id))
            return result.scalar_one_or_none()

    async def get_post_by_id(self, post_id: int) -> Optional[Post]:
        """Get post by database ID."""
        async with self.async_session() as session:
            return await session.get(Post, post_id)

    async def toggle_post(self, post_id: int) -> Optional[bool]:
        """Toggle post active status. Returns new status or None if not found."""
        async with self.async_session() as session:
            post = await session.get(Post, post_id)
            if post:
                post.is_active = not post.is_active
                await session.commit()
                logger.info(f"Post {post_id} toggled to {post.is_active}")
                return post.is_active
            return None

    async def delete_post(self, post_id: int) -> bool:
        """Delete post by ID."""
        async with self.async_session() as session:
            post = await session.get(Post, post_id)
            if post:
                await session.delete(post)
                await session.commit()
                logger.info(f"Post {post_id} deleted")
                return True
            return False

    # === Keywords ===

    async def get_all_keywords(self) -> List[Keyword]:
        """Get all keywords."""
        async with self.async_session() as session:
            result = await session.execute(select(Keyword).order_by(Keyword.created_at.desc()))
            return list(result.scalars().all())

    async def get_active_keywords(self) -> List[Keyword]:
        """Get all active keywords."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Keyword).where(Keyword.is_active == True).order_by(Keyword.word)
            )
            return list(result.scalars().all())

    async def add_keyword(self, word: str, match_type: str = "contains") -> Keyword:
        """Add new keyword."""
        async with self.async_session() as session:
            keyword = Keyword(word=word.lower().strip(), match_type=MatchType(match_type))
            session.add(keyword)
            await session.commit()
            await session.refresh(keyword)
            logger.info(f"Keyword added: {word}")
            return keyword

    async def get_keyword_by_word(self, word: str) -> Optional[Keyword]:
        """Get keyword by word."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Keyword).where(Keyword.word == word.lower().strip())
            )
            return result.scalar_one_or_none()

    async def toggle_keyword(self, keyword_id: int) -> Optional[bool]:
        """Toggle keyword active status."""
        async with self.async_session() as session:
            keyword = await session.get(Keyword, keyword_id)
            if keyword:
                keyword.is_active = not keyword.is_active
                await session.commit()
                return keyword.is_active
            return None

    async def delete_keyword(self, keyword_id: int) -> bool:
        """Delete keyword by ID."""
        async with self.async_session() as session:
            keyword = await session.get(Keyword, keyword_id)
            if keyword:
                await session.delete(keyword)
                await session.commit()
                logger.info(f"Keyword {keyword_id} deleted")
                return True
            return False

    # === Templates ===

    async def get_all_templates(self) -> List[MessageTemplate]:
        """Get all message templates."""
        async with self.async_session() as session:
            result = await session.execute(
                select(MessageTemplate).order_by(MessageTemplate.created_at.desc())
            )
            return list(result.scalars().all())

    async def add_template(self, name: str, content: str) -> MessageTemplate:
        """Add new message template."""
        async with self.async_session() as session:
            template = MessageTemplate(name=name.strip(), content=content)
            session.add(template)
            await session.commit()
            await session.refresh(template)
            logger.info(f"Template added: {name}")
            return template

    async def get_template_by_id(self, template_id: int) -> Optional[MessageTemplate]:
        """Get template by ID."""
        async with self.async_session() as session:
            return await session.get(MessageTemplate, template_id)

    async def delete_template(self, template_id: int) -> bool:
        """Delete template by ID."""
        async with self.async_session() as session:
            template = await session.get(MessageTemplate, template_id)
            if template:
                await session.delete(template)
                await session.commit()
                logger.info(f"Template {template_id} deleted")
                return True
            return False

    # === Rules ===

    async def get_all_rules(self) -> List[Rule]:
        """Get all rules with relationships loaded."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Rule)
                .options(
                    selectinload(Rule.post),
                    selectinload(Rule.keyword),
                    selectinload(Rule.template),
                )
                .order_by(Rule.created_at.desc())
            )
            return list(result.scalars().all())

    async def get_active_rules(self) -> List[Rule]:
        """Get all active rules with relationships loaded."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Rule)
                .where(Rule.is_active == True)
                .options(
                    selectinload(Rule.post),
                    selectinload(Rule.keyword),
                    selectinload(Rule.template),
                )
            )
            return list(result.scalars().all())

    async def add_rule(
        self, keyword_id: int, template_id: int, post_id: Optional[int] = None
    ) -> Rule:
        """Add new rule linking keyword to template."""
        async with self.async_session() as session:
            rule = Rule(post_id=post_id, keyword_id=keyword_id, template_id=template_id)
            session.add(rule)
            await session.commit()
            await session.refresh(rule)
            logger.info(f"Rule added: keyword={keyword_id}, template={template_id}, post={post_id}")
            return rule

    async def toggle_rule(self, rule_id: int) -> Optional[bool]:
        """Toggle rule active status."""
        async with self.async_session() as session:
            rule = await session.get(Rule, rule_id)
            if rule:
                rule.is_active = not rule.is_active
                await session.commit()
                return rule.is_active
            return None

    async def delete_rule(self, rule_id: int) -> bool:
        """Delete rule by ID."""
        async with self.async_session() as session:
            rule = await session.get(Rule, rule_id)
            if rule:
                await session.delete(rule)
                await session.commit()
                logger.info(f"Rule {rule_id} deleted")
                return True
            return False

    # === Processed Comments ===

    async def is_comment_processed(self, comment_id: str) -> bool:
        """Check if comment was already processed."""
        async with self.async_session() as session:
            result = await session.execute(
                select(ProcessedComment).where(ProcessedComment.comment_id == comment_id)
            )
            return result.scalar_one_or_none() is not None

    async def mark_comment_processed(self, comment_id: str) -> None:
        """Mark comment as processed."""
        async with self.async_session() as session:
            session.add(ProcessedComment(comment_id=comment_id))
            await session.commit()

    # === Sent Messages ===

    async def has_user_received_message(self, user_id: str, post_id: int) -> bool:
        """Check if user already received message for this post."""
        async with self.async_session() as session:
            result = await session.execute(
                select(SentMessage).where(
                    SentMessage.instagram_user_id == user_id,
                    SentMessage.post_id == post_id,
                    SentMessage.status == MessageStatus.SENT,
                )
            )
            return result.scalar_one_or_none() is not None

    async def log_sent_message(
        self,
        user_id: str,
        username: str,
        post_id: int,
        rule_id: int,
        status: str,
    ) -> SentMessage:
        """Log sent message."""
        async with self.async_session() as session:
            msg = SentMessage(
                instagram_user_id=user_id,
                username=username,
                post_id=post_id,
                rule_id=rule_id,
                status=MessageStatus(status),
            )
            session.add(msg)
            await session.commit()
            return msg

    async def get_messages_sent_last_hour(self) -> int:
        """Get count of messages sent in the last hour."""
        async with self.async_session() as session:
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            result = await session.execute(
                select(SentMessage).where(
                    SentMessage.sent_at >= one_hour_ago,
                    SentMessage.status == MessageStatus.SENT,
                )
            )
            return len(result.scalars().all())

    # === Statistics ===

    async def get_stats(self) -> Dict:
        """Get bot statistics."""
        async with self.async_session() as session:
            posts = await session.execute(select(Post))
            active_posts = await session.execute(select(Post).where(Post.is_active == True))
            keywords = await session.execute(select(Keyword))
            templates = await session.execute(select(MessageTemplate))
            rules = await session.execute(select(Rule))
            sent = await session.execute(
                select(SentMessage).where(SentMessage.status == MessageStatus.SENT)
            )
            processed = await session.execute(select(ProcessedComment))

            return {
                "total_posts": len(posts.scalars().all()),
                "active_posts": len(active_posts.scalars().all()),
                "total_keywords": len(keywords.scalars().all()),
                "total_templates": len(templates.scalars().all()),
                "total_rules": len(rules.scalars().all()),
                "total_sent": len(sent.scalars().all()),
                "total_comments_processed": len(processed.scalars().all()),
                "sent_last_hour": await self.get_messages_sent_last_hour(),
            }
    # === Welcome Settings ===

    async def get_welcome_settings(self) -> Optional[WelcomeSettings]:
        """Get welcome message settings."""
        async with self.async_session() as session:
            result = await session.execute(select(WelcomeSettings).limit(1))
            return result.scalar_one_or_none()

    async def set_welcome_message(self, message: str) -> WelcomeSettings:
        """Set welcome message text."""
        async with self.async_session() as session:
            result = await session.execute(select(WelcomeSettings).limit(1))
            settings = result.scalar_one_or_none()
            if settings:
                settings.message = message
                settings.updated_at = datetime.utcnow()
            else:
                settings = WelcomeSettings(message=message, is_enabled=False)
                session.add(settings)
            await session.commit()
            await session.refresh(settings)
            logger.info("Welcome message updated")
            return settings

    async def toggle_welcome(self) -> bool:
        """Toggle welcome message enabled status."""
        async with self.async_session() as session:
            result = await session.execute(select(WelcomeSettings).limit(1))
            settings = result.scalar_one_or_none()
            if settings:
                settings.is_enabled = not settings.is_enabled
                settings.updated_at = datetime.utcnow()
            else:
                settings = WelcomeSettings(is_enabled=True, message="")
                session.add(settings)
            await session.commit()
            await session.refresh(settings)
            status = "enabled" if settings.is_enabled else "disabled"
            logger.info(f"Welcome messages {status}")
            return settings.is_enabled

    # === Processed Followers ===

    async def is_follower_welcomed(self, user_id: str) -> bool:
        """Check if follower was already welcomed."""
        async with self.async_session() as session:
            result = await session.execute(
                select(ProcessedFollower).where(ProcessedFollower.instagram_user_id == user_id)
            )
            return result.scalar_one_or_none() is not None

    async def mark_follower_welcomed(self, user_id: str, username: str) -> None:
        """Mark follower as welcomed."""
        async with self.async_session() as session:
            session.add(ProcessedFollower(instagram_user_id=user_id, username=username))
            await session.commit()

    async def get_welcomed_followers_count(self) -> int:
        """Get count of welcomed followers."""
        async with self.async_session() as session:
            result = await session.execute(select(ProcessedFollower))
            return len(result.scalars().all())

    # === Broadcasts ===

    async def create_broadcast(
        self,
        name: str,
        message: str,
        segment_type: str,
        segment_filter: Optional[str] = None,
    ) -> Broadcast:
        """Create a new broadcast campaign."""
        async with self.async_session() as session:
            broadcast = Broadcast(
                name=name,
                message=message,
                segment_type=SegmentType(segment_type),
                segment_filter=segment_filter,
            )
            session.add(broadcast)
            await session.commit()
            await session.refresh(broadcast)
            logger.info(f"Broadcast created: {name}")
            return broadcast

    async def get_broadcast(self, broadcast_id: int) -> Optional[Broadcast]:
        """Get broadcast by ID with recipients."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Broadcast)
                .where(Broadcast.id == broadcast_id)
                .options(selectinload(Broadcast.recipients))
            )
            return result.scalar_one_or_none()

    async def get_all_broadcasts(self) -> List[Broadcast]:
        """Get all broadcasts."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Broadcast).order_by(Broadcast.created_at.desc())
            )
            return list(result.scalars().all())

    async def get_active_broadcasts(self) -> List[Broadcast]:
        """Get broadcasts that are in progress."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Broadcast).where(Broadcast.status == BroadcastStatus.IN_PROGRESS)
            )
            return list(result.scalars().all())

    async def update_broadcast_status(
        self, broadcast_id: int, status: str
    ) -> Optional[Broadcast]:
        """Update broadcast status."""
        async with self.async_session() as session:
            broadcast = await session.get(Broadcast, broadcast_id)
            if broadcast:
                broadcast.status = BroadcastStatus(status)
                if status == "in_progress" and not broadcast.started_at:
                    broadcast.started_at = datetime.utcnow()
                elif status in ("completed", "cancelled"):
                    broadcast.completed_at = datetime.utcnow()
                await session.commit()
                await session.refresh(broadcast)
                logger.info(f"Broadcast {broadcast_id} status: {status}")
            return broadcast

    async def add_broadcast_recipients(
        self, broadcast_id: int, users: List[Dict]
    ) -> int:
        """Add recipients to broadcast.

        Args:
            broadcast_id: Broadcast ID
            users: List of dicts with user_id and username

        Returns:
            Number of recipients added
        """
        async with self.async_session() as session:
            broadcast = await session.get(Broadcast, broadcast_id)
            if not broadcast:
                return 0

            count = 0
            for user in users:
                recipient = BroadcastRecipient(
                    broadcast_id=broadcast_id,
                    instagram_user_id=user["user_id"],
                    username=user["username"],
                )
                session.add(recipient)
                count += 1

            broadcast.total_users = count
            await session.commit()
            logger.info(f"Added {count} recipients to broadcast {broadcast_id}")
            return count

    async def get_pending_recipients(
        self, broadcast_id: int, limit: int = 10
    ) -> List[BroadcastRecipient]:
        """Get pending recipients for a broadcast."""
        async with self.async_session() as session:
            result = await session.execute(
                select(BroadcastRecipient)
                .where(
                    BroadcastRecipient.broadcast_id == broadcast_id,
                    BroadcastRecipient.status == MessageStatus.PENDING,
                )
                .limit(limit)
            )
            return list(result.scalars().all())

    async def update_recipient_status(
        self,
        recipient_id: int,
        status: str,
        error_message: Optional[str] = None,
    ) -> None:
        """Update recipient send status."""
        async with self.async_session() as session:
            recipient = await session.get(BroadcastRecipient, recipient_id)
            if recipient:
                recipient.status = MessageStatus(status)
                if status == "sent":
                    recipient.sent_at = datetime.utcnow()
                if error_message:
                    recipient.error_message = error_message
                await session.commit()

    async def increment_broadcast_counts(
        self, broadcast_id: int, sent: int = 0, failed: int = 0
    ) -> None:
        """Increment broadcast sent/failed counts."""
        async with self.async_session() as session:
            broadcast = await session.get(Broadcast, broadcast_id)
            if broadcast:
                broadcast.sent_count += sent
                broadcast.failed_count += failed
                await session.commit()

    async def get_users_by_keyword(self, keyword_id: int) -> List[Dict]:
        """Get users who commented with specific keyword.

        Returns list of unique users from sent_messages with given rule's keyword.
        """
        async with self.async_session() as session:
            # Get rules for this keyword
            rules_result = await session.execute(
                select(Rule).where(Rule.keyword_id == keyword_id)
            )
            rules = rules_result.scalars().all()
            rule_ids = [r.id for r in rules]

            if not rule_ids:
                return []

            # Get unique users from sent_messages
            result = await session.execute(
                select(SentMessage.instagram_user_id, SentMessage.username)
                .where(SentMessage.rule_id.in_(rule_ids))
                .distinct()
            )
            return [{"user_id": row[0], "username": row[1]} for row in result.all()]

    async def get_recent_followers(self, days: int = 7) -> List[Dict]:
        """Get followers welcomed in the last N days."""
        async with self.async_session() as session:
            cutoff = datetime.utcnow() - timedelta(days=days)
            result = await session.execute(
                select(ProcessedFollower)
                .where(ProcessedFollower.welcomed_at >= cutoff)
            )
            followers = result.scalars().all()
            return [{"user_id": f.instagram_user_id, "username": f.username} for f in followers]

    async def get_all_commenters(self) -> List[Dict]:
        """Get all unique users who received messages."""
        async with self.async_session() as session:
            result = await session.execute(
                select(SentMessage.instagram_user_id, SentMessage.username)
                .where(SentMessage.status == MessageStatus.SENT)
                .distinct()
            )
            return [{"user_id": row[0], "username": row[1]} for row in result.all()]

    async def delete_broadcast(self, broadcast_id: int) -> bool:
        """Delete broadcast by ID."""
        async with self.async_session() as session:
            broadcast = await session.get(Broadcast, broadcast_id)
            if broadcast:
                await session.delete(broadcast)
                await session.commit()
                logger.info(f"Broadcast {broadcast_id} deleted")
                return True
            return False
