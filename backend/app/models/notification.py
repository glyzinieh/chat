from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Column, Index
from sqlalchemy import JSON


class Notification(SQLModel, table=True):
    __table_args__ = (
        Index("ix_notification_user_id_created_at", "user_id", "created_at"),
        Index("ix_notification_user_id_read_at", "user_id", "read_at"),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    type: str  # e.g., "mention", "reply", "reaction"
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON))
    read_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
