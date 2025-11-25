from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class Follow(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    channel_id: int = Field(foreign_key="channel.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
