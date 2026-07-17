from typing import Annotated

from fastapi import APIRouter, Depends, status

from deps.auth import get_auth_user
from deps.board.board import (
    get_all_boards,
    get_authorized_board_or_404,
    get_board_service,
)
from deps.board.member import require_board_member_editor_role
from models import BoardModel, UserModel
from schemas import BoardCreate, BoardResponse, BoardUpdate
from services.board import BoardService

from .members import router as members_router

# tasks are a subcollection of boards
from .tasks import router as tasks_router

router = APIRouter(
    prefix="/boards", tags=["Boards"], dependencies=[Depends(get_auth_user)]
)


# Read all boards
@router.get("", response_model=list[BoardResponse])
async def read_all_boards(
    boards: Annotated[list[BoardModel], Depends(get_all_boards)],
):
    return boards


# Read board
@router.get(
    "/{id}",
    response_model=BoardResponse,
)
async def read_board(
    board: Annotated[BoardModel, Depends(get_authorized_board_or_404)],
):
    return board


# Create board
@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    board: BoardCreate,
    board_service: Annotated[BoardService, Depends(get_board_service)],
    auth_user: Annotated[UserModel, Depends(get_auth_user)],
):
    return board_service.create_board(board, auth_user.id)


# Update board (only editors can update)
@router.put(
    "/{id}",
    response_model=BoardResponse,
    dependencies=[
        Depends(require_board_member_editor_role),
    ],
)
async def update_board(
    board: Annotated[BoardModel, Depends(get_authorized_board_or_404)],
    updates: BoardUpdate,
    board_service: Annotated[BoardService, Depends(get_board_service)],
):
    return board_service.update_board(board, updates)


# Delete board
@router.delete("/{id}", dependencies=[Depends(require_board_member_editor_role)])
async def delete_board(
    board: Annotated[BoardModel, Depends(get_authorized_board_or_404)],
    board_service: Annotated[BoardService, Depends(get_board_service)],
):
    return board_service.delete_board(board)


router.include_router(tasks_router)
router.include_router(members_router)
