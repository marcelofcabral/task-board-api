from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# General
class ResponseSchemaBase:
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# User-related classes
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


# Board-related classes
class BoardBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=50)


class BoardResponse(BoardBase, ResponseSchemaBase):
    pass


# Task-related classes
class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=200)


class TaskCreate(TaskBase):
    user_id: int
    board_id: int


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=200)
    user_id: int | None = None
    board_id: int | None = None


class TaskResponse(TaskBase, ResponseSchemaBase):
    user: UserResponse
    board: BoardResponse
