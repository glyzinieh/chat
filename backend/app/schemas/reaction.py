from datetime import datetime
from sqlmodel import SQLModel


class ReactionBase(SQLModel):
    message_id: int
    type: str


class ReactionPublic(ReactionBase):
    id: int
    user_id: int
    created_at: datetime


class ReactionCreate(ReactionBase):
    pass
