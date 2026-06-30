from typing import Annotated

from fastapi import APIRouter, Depends

from auth.types import LoginResult
from deps.auth import get_auth_user, get_login_data
from models import UserModel
from schemas import UserResponse
from schemas.auth import LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=LoginResponse)
async def login(
    login_data: Annotated[LoginResult, Depends(get_login_data)],
):
    user, token = login_data

    return {"user": user, "access_token": token, "token_type": "JWT"}


@router.get("/me", response_model=UserResponse)
async def read_user_me(user: Annotated[UserModel, Depends(get_auth_user)]):
    return user
