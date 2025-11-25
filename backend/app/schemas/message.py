from datetime import datetime
from sqlmodel import SQLModel


class MessageBase(SQLModel):
    content: str
    parent_id: int | None = None


class MessagePublic(MessageBase):
    id: int
    channel_id: int
    author_id: int
    thread_root_id: int | None
    reply_count: int
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None


class MessageCreate(MessageBase):
    """Create schema for posting a message.
    
    Note: channel_id is extracted from URL path (e.g., POST /channels/{channel_id}/messages),
    author_id from authentication context
    """
    pass


class MessageUpdate(SQLModel):
    content: str | None = None
