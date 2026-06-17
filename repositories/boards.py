from models import BoardModel
from schemas import BoardCreate, BoardUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_board(id: int, db: Session) -> BoardModel:
    return db.get(BoardModel, id)


def list_boards(db: Session) -> list[BoardModel]:
    return db.scalars(select(BoardModel)).all()


def create_board(board: BoardCreate, db: Session) -> BoardModel:
    new_board = BoardModel(**board.model_dump())

    db.add(new_board)
    db.commit()
    db.refresh(new_board)

    return new_board


def update_board(id: int, board: BoardUpdate, db: Session) -> BoardModel:
    db_board = db.get(BoardModel, id)

    if db_board is None:
        return None

    for field, value in board.model_dump(exclude_unset=True).items():
        setattr(db_board, field, value)

    db.commit()
    db.refresh(db_board)

    return db_board


def delete_board(id: int, db: Session):
    db_board = db.get(BoardModel, id)

    if db_board is None:
        return None

    db.delete(db_board)
    db.commit()

    return db_board
