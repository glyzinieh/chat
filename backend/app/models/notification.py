from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Column, Field, Relationship, SQLModel
from sqlalchemy import JSON

if TYPE_CHECKING:
    from .user import User


class Notification(SQLModel, table=True):
    """Notification model for user notifications.
    
    Stores various types of notifications (mentions, replies, etc.)
    with JSON payload for flexible data storage.
    """
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    type: str  # "mention", "reply", "reaction", etc.
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON))
    read_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user: "User" = Relationship(back_populates="notifications")
