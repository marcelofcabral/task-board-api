from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import UserModel
from repositories import UserRepository
from services import UserService


def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)


def get_user_or_404(
    id: int, service: Annotated[UserService, Depends(get_user_service)]
) -> UserModel:
    user = service.get_user(id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


def get_all_users(
    service: Annotated[UserService, Depends(get_user_service)],
) -> list[UserModel]:
    return service.list_users()
