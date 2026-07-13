from typing import Annotated

from fastapi import APIRouter, Depends, status

from deps.board.member import (
    ensure_board_member_does_not_exist,
    get_all_board_members,
    get_auth_board_member_or_403,
    get_board_member_or_404,
    require_board_member_editor_role,
)
from deps.service_factories import get_board_member_service
from models import BoardMemberModel, UserModel
from schemas import (
    BoardMemberCreate,
    BoardMemberResponse,
    BoardMemberUpdate,
    UserResponse,
)
from services import BoardMemberService

router = APIRouter(
    prefix="/{board_id}/members",
    dependencies=[Depends(get_auth_board_member_or_403)],
)


# Read all board members
@router.get("", response_model=list[UserResponse])
async def read_all_board_members(
    members: Annotated[list[UserModel], Depends(get_all_board_members)],
):
    return members


# Get specific board member
@router.get("/{user_id}", response_model=UserResponse)
async def read_board_member(
    member: Annotated[UserModel, Depends(get_board_member_or_404)],
):
    return member


# Create a board member
@router.post(
    "",
    response_model=BoardMemberResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_board_member_editor_role),
        Depends(ensure_board_member_does_not_exist),
    ],
)
async def create_board_member(
    member: BoardMemberCreate,
    board_id: int,
    board_member_service: Annotated[
        BoardMemberService, Depends(get_board_member_service)
    ],
):
    return board_member_service.create_board_member(member, board_id)


# Update board member
@router.put(
    "/{user_id}",
    response_model=BoardMemberResponse,
    dependencies=[Depends(require_board_member_editor_role)],
)
async def update_board_member(
    member: Annotated[BoardMemberModel, Depends(get_board_member_or_404)],
    updates: BoardMemberUpdate,
    service: Annotated[BoardMemberService, Depends(get_board_member_service)],
):
    return service.update_board_member(member, updates)


# Delete board member
@router.delete("/{id}", dependencies=[Depends(require_board_member_editor_role)])
async def delete_board_member(
    member: Annotated[BoardMemberModel, Depends(get_board_member_or_404)],
    service: Annotated[BoardMemberService, Depends(get_board_member_service)],
):
    return service.delete_board_member(member)
