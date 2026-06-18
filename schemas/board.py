from pydantic import BaseModel, Field

from .common import ResponseSchemaBase


class BoardBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=50)


class BoardResponse(BoardBase, ResponseSchemaBase):
    pass
