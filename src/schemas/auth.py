from datetime import datetime

from pydantic import BaseModel, Field

from .user import UserResponse


class TokenData(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(TokenData, BaseModel):
    user: UserResponse


class RegistrationData(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=5, max_length=20)
    birth: datetime
