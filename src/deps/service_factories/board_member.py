from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import BoardMemberRepository
from services import BoardMemberService


def get_board_member_repository(
    db: Annotated[Session, Depends(get_db)],
) -> BoardMemberRepository:
    return BoardMemberRepository(db)


def get_board_member_service(
    repository: Annotated[BoardMemberRepository, Depends(get_board_member_repository)],
) -> BoardMemberService:
    return BoardMemberService(repository)
