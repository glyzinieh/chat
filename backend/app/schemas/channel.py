from datetime import datetime
from typing import Literal
from sqlmodel import SQLModel


class ChannelBase(SQLModel):
    slug: str
    name: str
    description: str | None = None
    visibility: Literal["public", "private"] = "public"


class ChannelPublic(ChannelBase):
    id: int
    owner_id: int
    created_at: datetime


class ChannelCreate(ChannelBase):
    pass


class ChannelUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    visibility: Literal["public", "private"] | None = None


class ChannelMemberBase(SQLModel):
    channel_id: int
    user_id: int
    role: Literal["owner", "admin", "member"] = "member"


class ChannelMemberPublic(ChannelMemberBase):
    id: int
    joined_at: datetime


class ChannelMemberCreate(ChannelMemberBase):
    pass
