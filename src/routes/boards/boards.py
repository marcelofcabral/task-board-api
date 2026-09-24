from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.inputs.board.create_board_input import CreateBoardInput
from application.inputs.board.update_board_input import UpdateBoardInput
from application.ports.board_repository_port import BoardRepositoryPort
from application.usecases.board.create_board_usecase import CreateBoardUseCase
from application.usecases.board.update_board_usecase import UpdateBoardUseCase
from deps.auth import get_auth_user
from deps.board.board import (
    get_all_boards,
    get_authorized_board_or_404,
    get_board_repository,
    get_create_board_usecase,
    get_update_board_usecase,
)
from deps.board.member import require_board_member_editor_role
from domain.entities.board_entity import BoardEntity
from domain.entities.user_entity import UserEntity
from dtos import BoardCreate, BoardResponse, BoardUpdate

from .members import router as members_router

# tasks are a subcollection of boards
from .tasks import router as tasks_router

router = APIRouter(
    prefix="/boards", tags=["Boards"], dependencies=[Depends(get_auth_user)]
)


# Read all boards
@router.get("", response_model=list[BoardResponse])
async def read_all_boards(
    boards: Annotated[list[BoardEntity], Depends(get_all_boards)],
):
    return boards


# Read board
@router.get(
    "/{board_id}",
    response_model=BoardResponse,
)
async def read_board(
    board: Annotated[BoardEntity, Depends(get_authorized_board_or_404)],
):
    return board


# Create board
@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    board: BoardCreate,
    create_board_usecase: Annotated[
        CreateBoardUseCase, Depends(get_create_board_usecase)
    ],
    auth_user: Annotated[UserEntity, Depends(get_auth_user)],
):
    return create_board_usecase.execute(
        CreateBoardInput(creator_id=auth_user.id, title=board.title)
    )


# Update board (only editors can update)
@router.put(
    "/{board_id}",
    response_model=BoardResponse,
    dependencies=[
        Depends(require_board_member_editor_role),
    ],
)
async def update_board(
    board: Annotated[BoardEntity, Depends(get_authorized_board_or_404)],
    updates: BoardUpdate,
    update_board_usecase: Annotated[
        UpdateBoardUseCase, Depends(get_update_board_usecase)
    ],
):
    return update_board_usecase.execute(
        UpdateBoardInput(board_id=board.id, title=updates.title or board.title)
    )


# Delete board
@router.delete("/{board_id}", dependencies=[Depends(require_board_member_editor_role)])
async def delete_board(
    board: Annotated[BoardEntity, Depends(get_authorized_board_or_404)],
    board_repo: Annotated[BoardRepositoryPort, Depends(get_board_repository)],
):
    return board_repo.delete_board(board.id)


router.include_router(tasks_router)
router.include_router(members_router)
