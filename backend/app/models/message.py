from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Column, Index
from sqlalchemy import Integer


class Message(SQLModel, table=True):
    __table_args__ = (
        Index("ix_message_channel_id_created_at", "channel_id", "created_at"),
        Index("ix_message_thread_root_id_created_at", "thread_root_id", "created_at"),
        Index("ix_message_parent_id", "parent_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    channel_id: int = Field(foreign_key="channel.id")
    author_id: int = Field(foreign_key="user.id", index=True)
    parent_id: int | None = Field(default=None, foreign_key="message.id")
    thread_root_id: int | None = Field(default=None, foreign_key="message.id")
    content: str  # Markdown format
    reply_count: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
