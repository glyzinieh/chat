from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON


class Notification(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    type: str  # e.g., "mention", "reply", "reaction"
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON))
    read_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
