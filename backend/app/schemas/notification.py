from datetime import datetime
from sqlmodel import SQLModel


class NotificationBase(SQLModel):
    type: str
    payload: dict


class NotificationPublic(NotificationBase):
    id: int
    user_id: int
    read_at: datetime | None
    created_at: datetime


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationUpdate(SQLModel):
    read_at: datetime | None = None
