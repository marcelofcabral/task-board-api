from sqlalchemy import select
from sqlalchemy.orm import Session

from models import BoardModel
from schemas import BoardCreate, BoardUpdate


class BoardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_board(self, id: int) -> BoardModel | None:
        return self.db.get(BoardModel, id)

    def list_boards(self) -> list[BoardModel]:
        return list(self.db.scalars(select(BoardModel)).all())

    def add_board(self, board: BoardCreate) -> BoardModel:
        new_board = BoardModel(**board.model_dump())

        self.db.add(new_board)
        self.db.flush()
        self.db.refresh(new_board)

        return new_board

    def update_board(self, board: BoardModel, updates: BoardUpdate) -> BoardModel:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(board, field, value)

        self.db.commit()
        self.db.refresh(board)

        return board

    def delete_board(self, board: BoardModel) -> None:
        self.db.delete(board)
        self.db.commit()

    def commit(self) -> None:
        self.db.commit()
