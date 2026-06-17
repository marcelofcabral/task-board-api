from typing import Annotated

from database import get_db
from deps.boards import get_all_boards, get_board_or_404
from fastapi import APIRouter, Depends
from models import BoardModel
from schemas import BoardCreate, BoardResponse
from sqlalchemy.orm import Session

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
@router.post("")
async def create_board(board: BoardCreate, db: Annotated[Session, Depends(get_db)]):
    return new_board


# Update board
@router.put("/{id}")
async def update_board(id: int, board: Board, _=Depends(get_board_or_404)):
    store.boards[id] = board

    return board


# Delete board
@router.delete("/{id}")
async def delete_board(id: int, _=Depends(get_board_or_404)):
    board = store.boards[id]
    del store.boards[id]

    return board
