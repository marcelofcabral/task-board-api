from pydantic import BaseModel, Field

from .board import BoardResponse
from .common import ResponseSchemaBase
from .user import UserResponse


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
