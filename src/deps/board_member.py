from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from application.usecases.board_member.get_board_member_usecase import (
    GetBoardMemberUsecase,
)
from application.usecases.board_member.list_board_members_usecase import (
    ListBoardMembersUsecase,
)
from application.usecases.user.get_user_usecase import GetUserUseCase
from application.usecases.user.get_users_by_ids_usecase import GetUsersByIdsUsecase
from database import get_db
from deps.auth import get_auth_user
from deps.user import (
    get_get_user_usecase,
    get_get_users_by_ids_usecase,
)
from domain.entities.board_member_entity import BoardMemberEntity
from domain.entities.user_entity import UserEntity
from domain.exceptions.board_member import BoardMemberNotFoundException
from domain.exceptions.user import UserNotFoundException
from infra.adapters.sqlalchemy_board_member_repository import (
    SqlAlchemyBoardMemberRepository,
)
from shared.types.board_member import BoardMemberRole


def get_board_member_repository(
    db: Annotated[Session, get_db],
) -> BoardMemberRepositoryPort:
    return SqlAlchemyBoardMemberRepository(db)


def get_get_board_member_usecase(
    board_member_repo: Annotated[BoardMemberRepositoryPort,],
) -> GetBoardMemberUsecase:
    return GetBoardMemberUsecase(board_member_repo)


def get_list_board_members_usecase(
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, get_board_member_repository
    ],
) -> ListBoardMembersUsecase:
    return ListBoardMembersUsecase(board_member_repo)


def get_auth_board_member_or_403(
    board_id: int,
    auth_user: Annotated[UserEntity, Depends(get_auth_user)],
    get_board_member_usecase: Annotated[
        GetBoardMemberUsecase, Depends(get_get_board_member_usecase)
    ],
) -> BoardMemberEntity:
    try:
        board_member = get_board_member_usecase.execute(
            board_id=board_id, user_id=auth_user.id
        )

        return board_member
    except BoardMemberNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to this board",
        ) from exception


def require_board_member_editor_role(
    board_member: Annotated[BoardMemberEntity, Depends(get_auth_board_member_or_403)],
) -> None:
    if board_member.role != BoardMemberRole.EDITOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User cannot edit this board"
        )


def get_all_board_members(
    board_id: int,
    get_users_by_ids_usecase: Annotated[
        GetUsersByIdsUsecase, Depends(get_get_users_by_ids_usecase)
    ],
    list_board_members_usecase: Annotated[
        ListBoardMembersUsecase, Depends(get_list_board_members_usecase)
    ],
) -> list[UserEntity]:
    board_members_ids = [
        board_member.user_id
        for board_member in list_board_members_usecase.execute(board_id)
    ]

    return get_users_by_ids_usecase.execute(board_members_ids)


def get_board_member_or_404(
    board_id: int,
    user_id: int,
    get_user_usecase: Annotated[GetUserUseCase, Depends(get_get_user_usecase)],
    get_board_member_usecase: Annotated[
        GetBoardMemberUsecase, Depends(get_get_board_member_usecase)
    ],
) -> UserEntity:
    try:
        board_member = get_board_member_usecase.execute(user_id, board_id)
        user = get_user_usecase.execute(board_member.user_id)

        return user
    except (BoardMemberNotFoundException, UserNotFoundException) as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board member not found"
        ) from exception
