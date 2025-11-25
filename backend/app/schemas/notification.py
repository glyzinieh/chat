from datetime import datetime
from typing import Literal
from sqlmodel import SQLModel


class NotificationBase(SQLModel):
    """Base schema for notifications.
    
    Valid notification types and their expected payload structures:
    - "mention": {"message_id": int, "mentioned_by": int}
    - "reply": {"message_id": int, "replied_by": int}
    - "reaction": {"message_id": int, "reaction_type": str, "reacted_by": int}
    """
    type: Literal["mention", "reply", "reaction"]
    payload: dict


class NotificationPublic(NotificationBase):
    id: int
    user_id: int
    read_at: datetime | None
    created_at: datetime


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationUpdate(SQLModel):
    """Update schema for marking notifications as read.
    
    Note: read_at is automatically set to current time server-side
    when this endpoint is called
    """
    pass
