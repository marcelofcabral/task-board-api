from typing import Annotated

from fastapi import Depends, HTTPException, status

from deps.auth import get_auth_user
from deps.service_factories import get_board_member_service
from deps.user import get_user_service
from models import BoardMemberModel, UserModel
from schemas import BoardMemberCreate
from services import BoardMemberService, UserService
from shared.types.board_member import BoardMemberRole


def get_auth_board_member_or_403(
    board_id: int,
    auth_user: Annotated[UserModel, Depends(get_auth_user)],
    board_member_service: Annotated[
        BoardMemberService, Depends(get_board_member_service)
    ],
) -> BoardMemberModel:
    board_member = board_member_service.get_board_member(
        board_id=board_id, user_id=auth_user.id
    )

    if not board_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to this board",
        )

    return board_member


def require_board_member_editor_role(
    board_member: Annotated[BoardMemberModel, Depends(get_auth_board_member_or_403)],
) -> None:
    if board_member.role != BoardMemberRole.EDITOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User cannot edit this board"
        )


# "Board member" in the following deps does not refer to the DB entity board_member
# but rather the UserModel associated to a BoardMemberModel via id
# that's why all of them return UserModels


def ensure_board_member_does_not_exist(
    member: BoardMemberCreate,
    board_id: int,
    board_member_service: Annotated[
        BoardMemberService, Depends(get_board_member_service)
    ],
) -> None:
    board_member = board_member_service.get_board_member(member.user_id, board_id)

    if board_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already is a board member",
        )


def get_all_board_members(
    board_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
    board_member_service: Annotated[
        BoardMemberService, Depends(get_board_member_service)
    ],
) -> list[UserModel]:
    board_members_ids = [
        board_member.user_id
        for board_member in board_member_service.list_board_members(board_id)
    ]

    return user_service.get_users_by_ids(board_members_ids)


def get_board_member_or_404(
    board_id: int,
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
    board_member_service: Annotated[
        BoardMemberService, Depends(get_board_member_service)
    ],
) -> UserModel:
    board_member = board_member_service.get_board_member(user_id, board_id)

    if not board_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board member not found"
        )

    user = user_service.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
