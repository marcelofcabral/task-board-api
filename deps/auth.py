from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import oauth2_scheme
from auth.types import LoginResult
from deps.user import get_user_repository
from models import UserModel
from repositories import UserRepository
from services import AuthService


def get_unauthorized_exception(detail: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(user_repository)


def get_login_data(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResult:
    login_result = auth_service.login(form_data)

    if not login_result:
        raise get_unauthorized_exception("Invalid username or password")

    user, token = login_result

    return LoginResult(user, token)


def get_auth_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserModel:
    user = user_service.get_auth_user(token)

    if not user:
        raise get_unauthorized_exception("Could not validate credentials")

    return user
