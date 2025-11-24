from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class UserProfileBase(SQLModel):
    name: str
    icon_url: str | None = None


class UserPublic(UserBase, UserProfileBase):
    id: int


class UserCreate(UserBase, UserProfileBase):
    password: str


class UserUpdate(UserBase, UserProfileBase):
    username: str | None = None
    password: str | None = None
    name: str | None = None
    icon_url: str | None = None
