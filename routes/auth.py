from typing import Annotated

from fastapi import APIRouter, Depends, status

from auth.types import LoginResult
from deps.auth import get_auth_service, get_auth_user, get_login_data
from models import UserModel
from schemas import UserResponse
from schemas.auth import LoginResponse, RegistrationData
from services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    registration_data: RegistrationData,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    auth_service.register(registration_data)


@router.post("/token", response_model=LoginResponse)
async def login(
    login_data: Annotated[LoginResult, Depends(get_login_data)],
):
    user, token = login_data

    return {"user": user, "access_token": token, "token_type": "Bearer"}


@router.get("/me", response_model=UserResponse)
async def read_user_me(user: Annotated[UserModel, Depends(get_auth_user)]):
    return user
