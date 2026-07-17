from pydantic import BaseModel, Field

from shared.types.board_member import BoardMemberRole


class BoardMemberBase(BaseModel):
    role: BoardMemberRole = Field(description="Board member role")


class BoardMemberCreate(BoardMemberBase):
    user_id: int


class BoardMemberUpdate(BoardMemberBase):
    pass


class BoardMemberResponse(BoardMemberCreate):
    pass
