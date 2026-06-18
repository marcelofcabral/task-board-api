from datetime import datetime

from pydantic import BaseModel, Field

from .common import ResponseSchemaBase


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    birth: datetime


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    birth: datetime | None = None


class UserResponse(UserBase, ResponseSchemaBase):
    pass
