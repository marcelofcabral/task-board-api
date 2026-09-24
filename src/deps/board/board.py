from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from application.ports.board_repository_port import BoardRepositoryPort
from application.ports.unit_of_work_port import UnitOfWorkPort
from application.ports.user_repository_port import UserRepositoryPort
from application.usecases.board.create_board_usecase import CreateBoardUseCase
from application.usecases.board.get_board_usecase import GetBoardUseCase
from application.usecases.board.list_boards_usecase import ListBoardsUseCase
from application.usecases.board.update_board_usecase import UpdateBoardUseCase
from database import get_db
from deps.auth import get_auth_user
from deps.board.member import get_auth_board_member_or_403
from deps.user import get_user_repository
from domain.entities.board_entity import BoardEntity
from domain.entities.board_member_entity import BoardMemberEntity
from domain.entities.user_entity import UserEntity
from domain.exceptions.board import BoardNotFoundException
from infra.adapters.sqlalchemy_board_member_repository import BoardMemberRepository
from infra.adapters.sqlalchemy_board_repository import SqlAlchemyBoardRepository
from infra.adapters.unit_of_work_adapter import UnitOfWorkAdapter


def get_board_repository(
    db: Annotated[Session, Depends(get_db)],
) -> BoardRepositoryPort:
    return SqlAlchemyBoardRepository(db)


def get_board_member_repository(
    db: Annotated[Session, Depends(get_db)],
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
    board_repo: Annotated[BoardRepositoryPort, Depends(get_board_repository)],
) -> BoardMemberRepositoryPort:
    return BoardMemberRepository(db, user_repo, board_repo)


def get_unit_of_work(
    db: Annotated[Session, Depends(get_db)],
) -> UnitOfWorkPort:
    return UnitOfWorkAdapter(db)


def get_list_boards_usecase(
    board_repo: Annotated[BoardRepositoryPort, Depends(get_board_repository)],
) -> ListBoardsUseCase:
    return ListBoardsUseCase(board_repo)


def get_get_board_usecase(
    board_repo: Annotated[BoardRepositoryPort, Depends(get_board_repository)],
) -> GetBoardUseCase:
    return GetBoardUseCase(board_repo)


def get_update_board_usecase(
    board_repo: Annotated[BoardRepositoryPort, Depends(get_board_repository)],
) -> UpdateBoardUseCase:
    return UpdateBoardUseCase(board_repo)


def get_create_board_usecase(
    board_repo: Annotated[BoardRepositoryPort, Depends(get_board_repository)],
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, Depends(get_board_member_repository)
    ],
    unit_of_work: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> CreateBoardUseCase:
    return CreateBoardUseCase(board_repo, board_member_repo, unit_of_work)


# authorize first using get_board_member_or_403 and only then check if board exists and return it
# this avoids leaking board IDs that exist or don't exist in the DB
def get_authorized_board_or_404(
    board_id: int,
    _: Annotated[BoardMemberEntity, Depends(get_auth_board_member_or_403)],
    get_board_usecase: Annotated[GetBoardUseCase, Depends(get_get_board_usecase)],
) -> BoardEntity:
    try:
        return get_board_usecase.execute(board_id)
    except BoardNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        ) from exception


def get_all_boards(
    auth_user: Annotated[UserEntity, Depends(get_auth_user)],
    list_boards_usecase: Annotated[
        ListBoardsUseCase, Depends(get_list_boards_usecase)
    ],
) -> list[BoardEntity]:
    return list_boards_usecase.execute(auth_user.id)
