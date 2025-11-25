from datetime import datetime
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    display_name: str


class UserPublic(UserBase):
    id: int
    created_at: datetime


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    username: str | None = None
    display_name: str | None = None
    password: str | None = None
