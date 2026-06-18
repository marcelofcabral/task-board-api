from typing import Annotated

from fastapi import APIRouter, Depends, status

from deps.user import get_all_users, get_user_or_404, get_user_service
from models import UserModel
from schemas import UserCreate, UserResponse, UserUpdate
from services import UserService

router = APIRouter(prefix="/user", tags=["Users"])


# Read all users
@router.get("", response_model=list[UserResponse])
async def read_all_users(users: Annotated[list[UserModel], Depends(get_all_users)]):
    return users


# Read user
@router.get("/{id}", response_model=UserResponse)
async def read_user(user: Annotated[UserModel, Depends(get_user_or_404)]):
    return user


# Create user
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, service: Annotated[UserService, Depends(get_user_service)]
):
    return service.create_user(user)


# Update user
@router.put("/{id}", response_model=UserResponse)
async def update_user(
    user: Annotated[UserModel, Depends(get_user_or_404)],
    updates: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return service.update_user(user, updates)


# Delete user
@router.delete("/{id}")
async def delete_user(
    user: Annotated[UserModel, Depends(get_user_or_404)],
    service: Annotated[UserService, Depends(get_user_service)],
):
    return service.delete_user(user)
