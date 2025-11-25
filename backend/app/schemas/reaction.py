from datetime import datetime
from typing import Literal
from sqlmodel import SQLModel


class ReactionBase(SQLModel):
    message_id: int
    type: Literal["thumbs_up", "heart", "laugh", "confused", "rocket", "eyes"]


class ReactionPublic(ReactionBase):
    id: int
    user_id: int
    created_at: datetime


class ReactionCreate(SQLModel):
    """Create schema for adding a reaction to a message.
    
    Note: message_id is extracted from URL path (e.g., POST /messages/{message_id}/reactions),
    user_id from authentication context
    """
    type: Literal["thumbs_up", "heart", "laugh", "confused", "rocket", "eyes"]
