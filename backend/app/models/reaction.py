from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Reaction(SQLModel, table=True):
    """Reaction model for emoji reactions to messages.
    
    Users can add emoji reactions to messages.
    """
    id: int | None = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="message.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    type: str  # Emoji type (e.g., "thumbs_up", "heart")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    message: "Message" = Relationship(back_populates="reactions")
    user: "User" = Relationship(back_populates="reactions")
