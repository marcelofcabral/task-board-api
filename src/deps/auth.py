from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from application.ports.user_repository_port import UserRepositoryPort
from application.usecases.auth.get_auth_user_usecase import GetAuthUserUseCase
from application.usecases.auth.login_user_usecase import LoginUserUseCase
from auth import oauth2_scheme
from auth.types import LoginResult
from deps.user import get_user_repository
from domain.entities.user_entity import UserEntity
from domain.exceptions.auth import InvalidTokenException


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


def get_login_user_usecase(
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> LoginUserUseCase:
    return LoginUserUseCase(user_repo)


def get_login_data(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_user_usecase: Annotated[LoginUserUseCase, Depends(get_login_user_usecase)],
) -> LoginResult:
    login_result = login_user_usecase.execute(form_data)

    if not login_result:
        raise get_unauthorized_exception("Invalid username or password")

    return login_result


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
