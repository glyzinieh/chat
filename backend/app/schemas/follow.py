from datetime import datetime
from sqlmodel import SQLModel


class FollowBase(SQLModel):
    user_id: int
    channel_id: int


class FollowPublic(FollowBase):
    id: int
    created_at: datetime


class FollowCreate(FollowBase):
    pass
