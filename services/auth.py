import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from auth import (
    ALGORITHM,
    SECRET_KEY,
    generate_token,
    get_hashed_password,
    verify_password,
)
from auth.types import LoginResult
from models import UserModel
from schemas import UserCreate
from schemas.auth import RegistrationData

from .user import UserService

# TODO: use domain exceptions to differentiate between invalid JWT (InvalidTokenError) and invalid credentials (InvalidCredentialsError or something like that)


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def authenticate_user(self, username: str, password: str) -> UserModel | None:
        user = self.user_service.get_user_by_username(username)

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user

    def get_auth_user(self, token: str) -> UserModel | None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")

            if username is None:
                return None

            user = self.user_service.get_user_by_username(username)

            return user

        except InvalidTokenError:
            return None

    def register(self, registration_data: RegistrationData):
        user = self.user_service.get_user_by_username(registration_data.username)

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            )

        hashed_password = get_hashed_password(registration_data.password)

        self.user_service.create_user(
            UserCreate(
                username=registration_data.username,
                hashed_password=hashed_password,
                birth=registration_data.birth,
            )
        )

    def login(self, form_data: OAuth2PasswordRequestForm) -> LoginResult | None:
        user = self.authenticate_user(form_data.username, form_data.password)

        if not user:
            return None

        token = generate_token({"sub": user.username})

        return LoginResult(user, token)
