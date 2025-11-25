from datetime import datetime
from sqlmodel import SQLModel


class FollowBase(SQLModel):
    user_id: int
    channel_id: int


class FollowPublic(FollowBase):
    id: int
    created_at: datetime


class FollowCreate(SQLModel):
    """Create schema for following a channel.
    
    Note: user_id extracted from authentication context,
    channel_id from URL path (e.g., POST /channels/{channel_id}/follow)
    """
    pass
