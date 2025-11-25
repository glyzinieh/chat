from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint


class Follow(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "channel_id", name="uq_follow_user_channel"),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    channel_id: int = Field(foreign_key="channel.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
