from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint


class Channel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", index=True)
    slug: str = Field(unique=True, index=True)
    name: str
    description: str | None = None
    visibility: str = Field(default="public")  # "public" or "private"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChannelMember(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("channel_id", "user_id", name="uq_channelmember_channel_user"),
    )

    id: int | None = Field(default=None, primary_key=True)
    channel_id: int = Field(foreign_key="channel.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(default="member")  # "owner", "admin", or "member"
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
