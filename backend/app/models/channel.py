from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .message import Message
    from .channel_member import ChannelMember
    from .follow import Follow


class ChannelVisibility(str, Enum):
    """Channel visibility options."""
    PUBLIC = "public"
    PRIVATE = "private"


class Channel(SQLModel, table=True):
    """Channel model for organizing conversations.
    
    Each user gets their own default channel, and can create additional channels.
    Channels can be public (anyone can view/post) or private (members only).
    """
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", index=True)
    slug: str = Field(unique=True, index=True)
    name: str
    description: str | None = None
    visibility: str = Field(default="public")  # "public" or "private"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    owner: "User" = Relationship(back_populates="owned_channels")
    messages: list["Message"] = Relationship(back_populates="channel")
    members: list["ChannelMember"] = Relationship(back_populates="channel")
    followers: list["Follow"] = Relationship(back_populates="channel")
