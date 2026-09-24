from datetime import UTC, datetime, timedelta
from typing import TypedDict

import jwt
from fastapi.security import OAuth2PasswordRequestForm

from application.ports.user_repository_port import UserRepositoryPort
from auth import ACCESS_TOKEN_EXPIRY_MINUTES, ALGORITHM, SECRET_KEY
from auth.types import LoginResult
from auth.utils import password_hasher
from domain.entities.user_entity import UserEntity
from domain.exceptions.auth import UserCredentialsIncorrectException


class JwtPayloadInput(TypedDict):
    sub: str


def generate_token(data_to_be_encoded: JwtPayloadInput) -> str:
    issued_at = datetime.now(UTC)
    expires_at = issued_at + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)

    payload = {
        **data_to_be_encoded,
        "exp": int(expires_at.timestamp()),
        "iat": int(issued_at.timestamp()),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_password(plaintext_password: str, hashed_password: str):
    return password_hasher.verify(plaintext_password, hashed_password)


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def _authenticate_user(self, username: str, password: str) -> UserEntity | None:
        user = self.user_repo.get_user_by_username(username)

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user

    def execute(self, form_data: OAuth2PasswordRequestForm) -> LoginResult:
        user = self._authenticate_user(form_data.username, form_data.password)

        if not user:
            raise UserCredentialsIncorrectException

        token = generate_token({"sub": str(user.id)})

        return LoginResult(user, token)
