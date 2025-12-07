"""SQLAlchemy database models."""

import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class MatchType(enum.Enum):
    """Keyword matching type."""

    EXACT = "exact"
    CONTAINS = "contains"
    REGEX = "regex"


class MessageStatus(enum.Enum):
    """Direct message status."""

    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Post(Base):
    """Monitored Instagram post."""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    instagram_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    url: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    rules: Mapped[List["Rule"]] = relationship(back_populates="post", cascade="all, delete-orphan")


class Keyword(Base):
    """Trigger keyword for comments."""

    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    match_type: Mapped[MatchType] = mapped_column(Enum(MatchType), default=MatchType.CONTAINS)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    rules: Mapped[List["Rule"]] = relationship(back_populates="keyword")


class MessageTemplate(Base):
    """Direct message template."""

    __tablename__ = "message_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    rules: Mapped[List["Rule"]] = relationship(back_populates="template")


class Rule(Base):
    """Rule linking keyword to message template."""

    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[Optional[int]] = mapped_column(ForeignKey("posts.id"), nullable=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keywords.id"))
    template_id: Mapped[int] = mapped_column(ForeignKey("message_templates.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    post: Mapped[Optional["Post"]] = relationship(back_populates="rules")
    keyword: Mapped["Keyword"] = relationship(back_populates="rules")
    template: Mapped["MessageTemplate"] = relationship(back_populates="rules")


class SentMessage(Base):
    """Log of sent Direct messages."""

    __tablename__ = "sent_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    instagram_user_id: Mapped[str] = mapped_column(String(50), index=True)
    username: Mapped[str] = mapped_column(String(100))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    rule_id: Mapped[int] = mapped_column(ForeignKey("rules.id"))
    status: Mapped[MessageStatus] = mapped_column(Enum(MessageStatus), default=MessageStatus.PENDING)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ProcessedComment(Base):
    """Log of processed comments to avoid duplicates."""

    __tablename__ = "processed_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    processed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WelcomeSettings(Base):
    """Settings for welcome messages to new followers."""

    __tablename__ = "welcome_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    message: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProcessedFollower(Base):
    """Log of processed followers to avoid duplicate welcome messages."""

    __tablename__ = "processed_followers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    instagram_user_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100))
    welcomed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BroadcastStatus(enum.Enum):
    """Broadcast status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SegmentType(enum.Enum):
    """User segment type for broadcasts."""

    KEYWORD_COMMENTERS = "keyword_commenters"  # Users who commented with specific keyword
    NEW_FOLLOWERS = "new_followers"  # New followers from last N days
    ALL_COMMENTERS = "all_commenters"  # All users who commented
    CUSTOM = "custom"  # Custom user list


class Broadcast(Base):
    """Mass broadcast campaign."""

    __tablename__ = "broadcasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    segment_type: Mapped[SegmentType] = mapped_column(Enum(SegmentType))
    segment_filter: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # keyword_id or days
    status: Mapped[BroadcastStatus] = mapped_column(Enum(BroadcastStatus), default=BroadcastStatus.PENDING)
    total_users: Mapped[int] = mapped_column(Integer, default=0)
    sent_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    recipients: Mapped[List["BroadcastRecipient"]] = relationship(
        back_populates="broadcast", cascade="all, delete-orphan"
    )


class BroadcastRecipient(Base):
    """Recipient for a broadcast."""

    __tablename__ = "broadcast_recipients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    broadcast_id: Mapped[int] = mapped_column(ForeignKey("broadcasts.id"))
    instagram_user_id: Mapped[str] = mapped_column(String(50), index=True)
    username: Mapped[str] = mapped_column(String(100))
    status: Mapped[MessageStatus] = mapped_column(Enum(MessageStatus), default=MessageStatus.PENDING)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    broadcast: Mapped["Broadcast"] = relationship(back_populates="recipients")
