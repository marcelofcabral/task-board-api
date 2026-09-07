from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from application.ports.board_repository_port import BoardRepositoryPort
from database import get_db
from deps.service_factories.board_member import get_board_member_service
from infra.adapters.sqlalchemy_board_repository import SqlAlchemyBoardRepository
from services import BoardMemberService, BoardService


def get_board_repository(
    db: Annotated[Session, Depends(get_db)],
) -> BoardRepositoryPort:
    return SqlAlchemyBoardRepository(db)


# TODO: finish this, add board member repository port and adapter


def get_list_boards_usecase(
    repository: Annotated[BoardRepositoryPort, Depends(get_board_repository)],
    board_member_service: Annotated[
        BoardMemberService, Depends(get_board_member_service)
    ],
) -> BoardService:
    return BoardService(repository, board_member_service)
