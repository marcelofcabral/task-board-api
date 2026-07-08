from datetime import datetime

from pydantic import BaseModel, Field

from .common import ResponseSchemaBase


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    birth: datetime


# internal schema: only used indirectly by the registration route
# (route handler -> auth service -> user service -> user repo)
class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    birth: datetime | None = None


# excludes the hashed password from the response body via the routes' response_model
class UserResponse(UserBase, ResponseSchemaBase):
    pass
