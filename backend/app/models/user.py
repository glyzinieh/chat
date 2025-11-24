from sqlmodel import Field, Relationship

from ..schemas.user import UserBase, UserProfileBase


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    profile: UserProfile = Relationship(
        back_populates="user",
        cascade_delete=True,
    )


class UserProfile(UserProfileBase, table=True):
    user_id: int = Field(foreign_key="user.id", unique=True, primary_key=True)

    user: User = Relationship(
        back_populates="profile", sa_relationship_kwargs={"uselist": False}
    )
