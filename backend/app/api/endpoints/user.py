from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import join, select

from ...core.security import get_password_hash
from ...models.user import User, UserProfile
from ...schemas.user import UserCreate, UserPublic, UserUpdate
from ..deps import SessionDep

router = APIRouter()


@router.post("/", response_model=UserPublic)
def create_user(user_create: UserCreate, session: SessionDep):
    user = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(user_create.password)
    user = User(
        username=user_create.username,
        hashed_password=hashed_password,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None

    profile = UserProfile(
        user_id=user.id,
        name=user_create.name,
        icon_url=user_create.icon_url,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)

    user.profile = profile
    return UserPublic(
        id=user.id,
        username=user.username,
        name=profile.name,
        icon_url=profile.icon_url,
    )


def map_user_to_public(user: User) -> UserPublic:
    assert user.id is not None
    return UserPublic(
        id=user.id,
        username=user.username,
        name=user.profile.name,
        icon_url=user.profile.icon_url,
    )


@router.get("/", response_model=list[UserPublic])
def read_users(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
):
    statement = select(User).offset(skip).limit(limit).join(UserProfile)
    users = session.exec(statement).all()
    return [*map(map_user_to_public, users)]


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    statement = select(User).where(User.id == user_id).join(UserProfile)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return map_user_to_public(user)


@router.put("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: SessionDep,
):
    statement = select(User).where(User.id == user_id).join(UserProfile)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user_update.username is not None:
        # Check for username uniqueness
        existing_user = session.exec(
            select(User).where(User.username == user_update.username)
        ).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        user.username = user_update.username
    if user_update.password is not None:
        user.hashed_password = get_password_hash(user_update.password)
    if user_update.name is not None:
        user.profile.name = user_update.name
    if user_update.icon_url is not None:
        user.profile.icon_url = user_update.icon_url

    session.add(user)
    session.commit()
    session.refresh(user)

    return map_user_to_public(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    session.delete(user)
    session.commit()
