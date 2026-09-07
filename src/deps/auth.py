from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from application.ports.user_repository_port import UserRepositoryPort
from application.usecases.auth.get_auth_user_usecase import GetAuthUserUseCase
from auth import oauth2_scheme
from auth.types import LoginResult
from deps.user import get_user_repository
from domain.entities.user_entity import UserEntity
from domain.exceptions.auth import InvalidTokenException
from services import AuthService


def get_unauthorized_exception(detail: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_get_auth_user_usecase(
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> GetAuthUserUseCase:
    return GetAuthUserUseCase(user_repo)


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
    get_auth_user_usecase: Annotated[
        GetAuthUserUseCase, Depends(get_get_auth_user_usecase)
    ],
) -> UserEntity:
    try:
        user = get_auth_user_usecase.execute(token)
        print(f"User is {user}")
    except InvalidTokenException as exception:
        raise get_unauthorized_exception(str(exception)) from exception

    return user
