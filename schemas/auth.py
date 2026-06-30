from pydantic import BaseModel

from schemas import UserResponse


class TokenData(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(TokenData, BaseModel):
    user: UserResponse
