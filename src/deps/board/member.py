from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from application.ports.unit_of_work_port import UnitOfWorkPort
from application.ports.user_repository_port import UserRepositoryPort
from database import get_db
from deps.auth import get_auth_user
from deps.user import get_user_repository
from domain.entities.board_member_entity import BoardMemberEntity
from domain.entities.user_entity import UserEntity
from domain.value_objects.board_member.board_member_patch import BoardMemberPatch
from domain.value_objects.board_member.new_board_member import NewBoardMember
from dtos import BoardMemberCreate, BoardMemberUpdate
from infra.adapters.sqlalchemy_board_member_repository import BoardMemberRepository
from infra.adapters.sqlalchemy_board_repository import SqlAlchemyBoardRepository
from infra.adapters.unit_of_work_adapter import UnitOfWorkAdapter
from shared.types.board_member import BoardMemberRole


def get_board_member_repository(
    db: Annotated[Session, Depends(get_db)],
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> BoardMemberRepositoryPort:
    return BoardMemberRepository(db, user_repo, SqlAlchemyBoardRepository(db))


def get_unit_of_work(
    db: Annotated[Session, Depends(get_db)],
) -> UnitOfWorkPort:
    return UnitOfWorkAdapter(db)


def get_auth_board_member_or_403(
    board_id: int,
    auth_user: Annotated[UserEntity, Depends(get_auth_user)],
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, Depends(get_board_member_repository)
    ],
) -> BoardMemberEntity:
    board_member = board_member_repo.get_board_member(
        user_id=auth_user.id, board_id=board_id
    )

    if not board_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to this board",
        )

    return board_member


def require_board_member_editor_role(
    board_member: Annotated[BoardMemberEntity, Depends(get_auth_board_member_or_403)],
) -> None:
    if board_member.role != BoardMemberRole.EDITOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User cannot edit this board"
        )


# "Board member" in the following deps does not refer to the membership row
# but rather the user associated to a board member via id


def ensure_board_member_does_not_exist(
    member: BoardMemberCreate,
    board_id: int,
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, Depends(get_board_member_repository)
    ],
) -> None:
    board_member = board_member_repo.get_board_member(member.user_id, board_id)

    if board_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already is a board member",
        )


def get_all_board_members(
    board_id: int,
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, Depends(get_board_member_repository)
    ],
) -> list[UserEntity]:
    board_members_ids = [
        board_member.user_id
        for board_member in board_member_repo.list_board_members(board_id)
    ]

    return user_repo.get_users_by_ids(board_members_ids)


def get_board_member_or_404(
    board_id: int,
    user_id: int,
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, Depends(get_board_member_repository)
    ],
) -> UserEntity:
    board_member = board_member_repo.get_board_member(user_id, board_id)

    if not board_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board member not found"
        )

    user = user_repo.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


def create_board_member(
    member: BoardMemberCreate,
    board_id: int,
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, Depends(get_board_member_repository)
    ],
    unit_of_work: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> BoardMemberEntity:
    board_member = board_member_repo.add_board_member(
        NewBoardMember(user_id=member.user_id, board_id=board_id, role=member.role)
    )
    unit_of_work.commit()

    return board_member


def update_board_member(
    board_id: int,
    user_id: int,
    updates: BoardMemberUpdate,
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, Depends(get_board_member_repository)
    ],
) -> BoardMemberEntity:
    return board_member_repo.update_board_member(
        BoardMemberPatch(user_id=user_id, board_id=board_id, role=updates.role)
    )


def delete_board_member(
    board_id: int,
    user_id: int,
    board_member_repo: Annotated[
        BoardMemberRepositoryPort, Depends(get_board_member_repository)
    ],
    unit_of_work: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> None:
    board_member_repo.delete_board_member(user_id, board_id)
    unit_of_work.commit()
