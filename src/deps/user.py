from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.user_repository_port import UserRepositoryPort
from application.usecases.user.create_user_usecase import CreateUserUseCase
from application.usecases.user.delete_user_usecase import DeleteUserUseCase
from application.usecases.user.get_user_usecase import GetUserUseCase
from application.usecases.user.list_users_usecase import ListUsersUseCase
from application.usecases.user.register_user_usecase import RegisterUserUsecase
from application.usecases.user.update_user_usecase import UpdateUserUseCase
from database import get_db
from domain.entities.user_entity import UserEntity
from infra.adapters.sqlalchemy_user_repository import SqlAlchemyUserRepository


def get_user_repository(
    db: Annotated[Session, Depends(get_db)],
) -> UserRepositoryPort:
    return SqlAlchemyUserRepository(db)


def get_get_user_usecase(
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> GetUserUseCase:
    return GetUserUseCase(user_repo)


def get_list_users_usecase(
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> ListUsersUseCase:
    return ListUsersUseCase(user_repo)


def get_register_user_usecase(
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> RegisterUserUsecase:
    return RegisterUserUsecase(user_repo)


def get_create_user_usecase(
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repo)


def get_update_user_usecase(
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repo)


def get_delete_user_usecase(
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_repo)


def get_user_or_404(
    id: int,
    get_user_usecase: Annotated[GetUserUseCase, Depends(get_get_user_usecase)],
) -> UserEntity:
    user = get_user_usecase.execute(id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


def get_all_users(
    list_users_usecase: Annotated[ListUsersUseCase, Depends(get_list_users_usecase)],
) -> list[UserEntity]:
    return list_users_usecase.execute()
