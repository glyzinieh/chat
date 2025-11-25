from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint


class Reaction(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("message_id", "user_id", "type", name="uq_reaction_message_user_type"),
    )

    id: int | None = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="message.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    type: str  # Emoji type, e.g., "thumbs_up", "heart"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
