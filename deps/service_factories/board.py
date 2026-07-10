from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from deps.service_factories.board_member import get_board_member_service
from repositories import BoardRepository
from services import BoardMemberService, BoardService


def get_board_repository(db: Annotated[Session, Depends(get_db)]) -> BoardRepository:
    return BoardRepository(db)


def get_board_service(
    repository: Annotated[BoardRepository, Depends(get_board_repository)],
    board_member_service: Annotated[
        BoardMemberService, Depends(get_board_member_service)
    ],
) -> BoardService:
    return BoardService(repository, board_member_service)
