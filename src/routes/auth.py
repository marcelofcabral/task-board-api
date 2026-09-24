from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from application.usecases.user.register_user_usecase import RegisterUserUsecase
from auth.types import LoginResult
from deps.auth import get_auth_user, get_login_data
from deps.user import get_register_user_usecase
from domain.entities.user_entity import UserEntity
from domain.exceptions.user import UserAlreadyExistsException
from dtos.auth import LoginResponse, RegistrationData
from dtos.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    registration_data: RegistrationData,
    register_user_usecase: Annotated[
        RegisterUserUsecase, Depends(get_register_user_usecase)
    ],
):
    try:
        register_user_usecase.execute(registration_data)
    except UserAlreadyExistsException as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exception)
        ) from exception


@router.post("/token", response_model=LoginResponse)
async def login(
    login_data: Annotated[LoginResult, Depends(get_login_data)],
):
    user, token = login_data

    return {"user": user, "access_token": token, "token_type": "Bearer"}


@router.get("/me", response_model=UserResponse)
async def read_user_me(user: Annotated[UserEntity, Depends(get_auth_user)]):
    return user
