from typing import Annotated

from fastapi import APIRouter, Depends, status

from deps.board import get_all_boards, get_board_or_404, get_board_service
from models import BoardModel
from schemas import BoardCreate, BoardResponse, BoardUpdate
from services.board import BoardService

router = APIRouter(prefix="/board", tags=["Boards"])


# Read all boards
@router.get("", response_model=list[BoardResponse])
async def read_all_boards(
    boards: Annotated[list[BoardModel], Depends(get_all_boards)],
):
    return boards


# Read board
@router.get("/{id}", response_model=BoardResponse)
async def read_board(board: Annotated[BoardModel, Depends(get_board_or_404)]):
    return board


# Create board
@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    board: BoardCreate, service: Annotated[BoardService, Depends(get_board_service)]
):
    return service.create_board(board)


# Update board
@router.put("/{id}", response_model=BoardResponse)
async def update_board(
    board: Annotated[BoardModel, Depends(get_board_or_404)],
    updates: BoardUpdate,
    service: Annotated[BoardService, Depends(get_board_service)],
):
    return service.update_board(board, updates)


# Delete board
@router.delete("/{id}")
async def delete_board(
    board: Annotated[BoardModel, Depends(get_board_or_404)],
    service: Annotated[BoardService, Depends(get_board_service)],
):
    return service.delete_board(board)
