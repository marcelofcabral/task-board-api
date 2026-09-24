from typing import Annotated

from fastapi import APIRouter, Depends, status

from deps.board.member import (
    create_board_member,
    delete_board_member,
    ensure_board_member_does_not_exist,
    get_all_board_members,
    get_auth_board_member_or_403,
    get_board_member_or_404,
    require_board_member_editor_role,
    update_board_member,
)
from domain.entities.board_member_entity import BoardMemberEntity
from domain.entities.user_entity import UserEntity
from dtos import BoardMemberResponse, UserResponse

router = APIRouter(
    prefix="/{board_id}/members",
    dependencies=[Depends(get_auth_board_member_or_403)],
)


# Read all board members
@router.get("", response_model=list[UserResponse])
async def read_all_board_members(
    members: Annotated[list[UserEntity], Depends(get_all_board_members)],
):
    return members


# Get specific board member
@router.get("/{user_id}", response_model=UserResponse)
async def read_board_member(
    member: Annotated[UserEntity, Depends(get_board_member_or_404)],
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
async def create_member(
    member: Annotated[BoardMemberEntity, Depends(create_board_member)],
):
    return member


# Update board member
@router.put(
    "/{user_id}",
    response_model=BoardMemberResponse,
    dependencies=[Depends(require_board_member_editor_role)],
)
async def update_member(
    member: Annotated[BoardMemberEntity, Depends(update_board_member)],
):
    return member


# Delete board member
@router.delete(
    "/{user_id}", dependencies=[Depends(require_board_member_editor_role)]
)
async def delete_member(
    _: Annotated[None, Depends(delete_board_member)],
):
    return None
