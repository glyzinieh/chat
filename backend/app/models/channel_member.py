from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .channel import Channel


class ChannelMember(SQLModel, table=True):
    """ChannelMember model for tracking membership in private channels.
    
    Used to control access to private channels.
    """
    id: int | None = Field(default=None, primary_key=True)
    channel_id: int = Field(foreign_key="channel.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(default="member")  # "owner", "admin", "member"
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    channel: "Channel" = Relationship(back_populates="members")
    user: "User" = Relationship(back_populates="channel_memberships")
