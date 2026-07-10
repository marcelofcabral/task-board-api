from typing import Annotated

from fastapi import Depends, HTTPException, status

from deps.auth import get_auth_user
from deps.service_factories import get_board_member_service
from models import BoardMemberModel, UserModel
from services import BoardMemberService
from shared.types.board_member import BoardMemberRole


def get_board_member_or_403(
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
    board_member: Annotated[BoardMemberModel, Depends(get_board_member_or_403)],
) -> None:
    if board_member.role != BoardMemberRole.EDITOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User cannot edit this board"
        )
