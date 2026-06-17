from typing import Annotated

from database import get_db
from fastapi import Depends, HTTPException, status
from models import BoardModel
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_board_or_404(id: int, db: Annotated[Session, Depends(get_db)]) -> BoardModel:
    board = db.get(BoardModel, id)

    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    return board


def get_all_boards(db: Annotated[Session, Depends(get_db)]) -> list[BoardModel]:
    boards = db.scalars(select(BoardModel)).all()

    return boards
