from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class Channel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", index=True)
    slug: str = Field(unique=True, index=True)
    name: str
    description: str | None = None
    visibility: str = Field(default="public")  # "public" or "private"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChannelMember(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    channel_id: int = Field(foreign_key="channel.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(default="member")  # "owner", "admin", or "member"
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
