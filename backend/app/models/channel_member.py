from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .channel import Channel


class MemberRole(str, Enum):
    """Channel member role options."""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class ChannelMember(SQLModel, table=True):
    """ChannelMember model for tracking membership in private channels.
    
    Used to control access to private channels.
    """
    __tablename__ = "channelmember"
    __table_args__ = (
        UniqueConstraint("channel_id", "user_id", name="uq_channelmember_channel_user"),
    )
    
    id: int | None = Field(default=None, primary_key=True)
    channel_id: int = Field(foreign_key="channel.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(default="member")  # "owner", "admin", or "member"
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    channel: "Channel" = Relationship(back_populates="members")
    user: "User" = Relationship(back_populates="channel_memberships")
