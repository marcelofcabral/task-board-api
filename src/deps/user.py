from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.user_repository_port import UserRepositoryPort
from application.usecases.user.get_user_usecase import GetUserUseCase
from application.usecases.user.get_users_by_ids_usecase import GetUsersByIdsUsecase
from application.usecases.user.list_users_usecase import ListUsersUsecase
from database import get_db
from domain.entities.user_entity import UserEntity
from infra.adapters.sqlalchemy_user_repository import SqlAlchemyUserRepository


def get_user_repository(
    db: Annotated[Session, Depends(get_db)],
) -> UserRepositoryPort:
    return SqlAlchemyUserRepository(db)


def get_get_user_usecase(
    repository: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> GetUserUseCase:
    return GetUserUseCase(repository)


def get_list_users_usecase(
    repository: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> ListUsersUsecase:
    return ListUsersUsecase(repository)


def get_get_users_by_ids_usecase(
    repository: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> GetUsersByIdsUsecase:
    return GetUsersByIdsUsecase(repository)


def get_user_or_404(
    id: int, get_user_usecase: Annotated[GetUserUseCase, Depends(get_get_user_usecase)]
) -> UserEntity:
    user = get_user_usecase.execute(id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


def get_all_users(
    list_users_usecase: Annotated[ListUsersUsecase, Depends(get_list_users_usecase)],
) -> list[UserEntity]:
    return list_users_usecase.execute()
