from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.inputs.user.create_user_input import CreateUserInput
from application.inputs.user.update_user_input import UpdateUserInput
from application.usecases.user.create_user_usecase import CreateUserUseCase
from application.usecases.user.delete_user_usecase import DeleteUserUseCase
from application.usecases.user.update_user_usecase import UpdateUserUseCase
from deps.auth import get_auth_user
from deps.user import (
    get_all_users,
    get_create_user_usecase,
    get_delete_user_usecase,
    get_update_user_usecase,
    get_user_or_404,
)
from domain.entities.user_entity import UserEntity
from dtos import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_auth_user)]
)


# Read all users
@router.get("", response_model=list[UserResponse])
async def read_all_users(
    users: Annotated[list[UserEntity], Depends(get_all_users)],
):
    return users


# Read user
@router.get("/{id}", response_model=UserResponse)
async def read_user(user: Annotated[UserEntity, Depends(get_user_or_404)]):
    return user


# Create user
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    create_user_usecase: Annotated[CreateUserUseCase, Depends(get_create_user_usecase)],
):
    return create_user_usecase.execute(
        CreateUserInput(
            username=user.username,
            hashed_password=user.hashed_password,
            birth=user.birth,
        )
    )


# Update user
@router.put("/{id}", response_model=UserResponse)
async def update_user(
    user: Annotated[UserEntity, Depends(get_user_or_404)],
    updates: UserUpdate,
    update_user_usecase: Annotated[UpdateUserUseCase, Depends(get_update_user_usecase)],
):
    return update_user_usecase.execute(
        UpdateUserInput(user_id=user.id, username=updates.username, birth=updates.birth)
    )


# Delete user
@router.delete("/{id}")
async def delete_user(
    user: Annotated[UserEntity, Depends(get_user_or_404)],
    delete_user_usecase: Annotated[DeleteUserUseCase, Depends(get_delete_user_usecase)],
):
    return delete_user_usecase.execute(user.id)
