from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.board_repository_port import BoardRepositoryPort
from application.usecases.board.get_board_usecase import GetBoardUseCase
from application.usecases.board.list_boards_usecase import ListBoardsUseCase
from database import get_db
from deps.board_member import get_auth_board_member_or_403
from domain.entities.board_entity import BoardEntity
from domain.exceptions.board import BoardNotFoundException
from infra.adapters.sqlalchemy_board_repository import SqlAlchemyBoardRepository


def get_board_repository(db: Annotated[Session, get_db]):
    return SqlAlchemyBoardRepository(db)


def get_get_board_usecase(
    repository: Annotated[BoardRepositoryPort, get_board_repository],
) -> GetBoardUseCase:
    return GetBoardUseCase(repository)


def get_list_boards_usecase(
    repository: Annotated[BoardRepositoryPort, get_board_repository],
) -> ListBoardsUseCase:
    return ListBoardsUseCase(repository)


# authorize first using get_board_member_or_403 and only then check if board exists and return it
# this avoids leaking board IDs that exist or don't exist in the DB
def get_authorized_board_or_404(
    board_id: int,
    _: Annotated[BoardEntity, Depends(get_auth_board_member_or_403)],
    get_board_usecase: Annotated[GetBoardUseCase, Depends(get_get_board_usecase)],
) -> BoardEntity:
    try:
        board = get_board_usecase.execute(board_id)

        return board
    except BoardNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        ) from exception


def get_all_boards(
    list_boards_usecase: Annotated[ListBoardsUseCase, Depends(get_list_boards_usecase)],
) -> list[BoardEntity]:
    return list_boards_usecase.execute()
