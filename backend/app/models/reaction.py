from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class Reaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="message.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    type: str  # Emoji type, e.g., "thumbs_up", "heart"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
