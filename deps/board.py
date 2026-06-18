from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import BoardModel
from repositories import BoardRepository
from services import BoardService


def get_board_repository(db: Annotated[Session, Depends(get_db)]) -> BoardRepository:
    return BoardRepository(db)


def get_board_service(
    repository: Annotated[BoardRepository, Depends(get_board_repository)],
) -> BoardService:
    return BoardService(repository)


def get_board_or_404(
    id: int, service: Annotated[BoardService, Depends(get_board_service)]
) -> BoardModel:
    board = service.get_board(id)

    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return board


def get_all_boards(
    service: Annotated[BoardService, Depends(get_board_service)],
) -> list[BoardModel]:
    return service.list_boards()
