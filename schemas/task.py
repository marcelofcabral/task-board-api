from pydantic import BaseModel, Field

from .common import ResponseSchemaBase


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=200)
    user_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=200)
    user_id: int | None = None


class TaskResponse(TaskBase, ResponseSchemaBase):
    id: int
