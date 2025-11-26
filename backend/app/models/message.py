from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .channel import Channel
    from .reaction import Reaction


class Message(SQLModel, table=True):
    """Message model for posts in channels.
    
    Supports threading with parent_id and thread_root_id:
    - parent_id: Direct parent message (for replies)
    - thread_root_id: Root message of the thread (for efficient thread queries)
    - reply_count: Denormalized count of replies for performance
    """
    id: int | None = Field(default=None, primary_key=True)
    channel_id: int = Field(foreign_key="channel.id", index=True)
    author_id: int = Field(foreign_key="user.id", index=True)
    parent_id: int | None = Field(default=None, foreign_key="message.id", index=True)
    thread_root_id: int | None = Field(default=None, foreign_key="message.id", index=True)
    content: str  # Markdown content
    reply_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    
    # Relationships
    channel: "Channel" = Relationship(back_populates="messages")
    author: "User" = Relationship(back_populates="messages")
    reactions: list["Reaction"] = Relationship(back_populates="message")
    
    # Self-referential relationships for threading
    parent: "Message | None" = Relationship(
        back_populates="replies",
        sa_relationship_kwargs={
            "remote_side": "Message.id",
            "foreign_keys": "[Message.parent_id]"
        }
    )
    replies: list["Message"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={
            "foreign_keys": "[Message.parent_id]"
        }
    )
    
    thread_root: "Message | None" = Relationship(
        back_populates="thread_messages",
        sa_relationship_kwargs={
            "remote_side": "Message.id",
            "foreign_keys": "[Message.thread_root_id]"
        }
    )
    thread_messages: list["Message"] = Relationship(
        back_populates="thread_root",
        sa_relationship_kwargs={
            "foreign_keys": "[Message.thread_root_id]"
        }
    )
