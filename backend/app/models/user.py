from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from ..schemas.user import UserBase, UserProfileBase

if TYPE_CHECKING:
    from . import UserProfile
    from .channel import Channel
    from .channel_member import ChannelMember
    from .follow import Follow
    from .message import Message
    from .reaction import Reaction
    from .notification import Notification


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    profile: "UserProfile" = Relationship(
        back_populates="user",
        cascade_delete=True,
    )
    
    # Channel relationships
    owned_channels: list["Channel"] = Relationship(back_populates="owner")
    channel_memberships: list["ChannelMember"] = Relationship(back_populates="user")
    follows: list["Follow"] = Relationship(back_populates="user")
    
    # Message relationships
    messages: list["Message"] = Relationship(back_populates="author")
    reactions: list["Reaction"] = Relationship(back_populates="user")
    
    # Notification relationships
    notifications: list["Notification"] = Relationship(back_populates="user")


class UserProfile(UserProfileBase, table=True):
    user_id: int = Field(foreign_key="user.id", unique=True, primary_key=True)

    user: User = Relationship(
        back_populates="profile", sa_relationship_kwargs={"uselist": False}
    )
