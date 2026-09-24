from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.board_repository_port import BoardRepositoryPort
from domain.entities.board_entity import BoardEntity
from domain.exceptions.board import BoardNotFoundException
from domain.value_objects.board.board_patch import BoardPatch
from domain.value_objects.board.new_board import NewBoard
from infra.mappers.entity_mappers import to_entities, to_entity
from infra.mappers.model_mappers import apply_patch_to_model
from infra.models import BoardModel


class SqlAlchemyBoardRepository(BoardRepositoryPort):
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def get_board(self, id: int) -> BoardEntity | None:
        db_board = self.db.get(BoardModel, id)

        if not db_board:
            return None

        return to_entity(db_board, BoardEntity)

    def get_board_by_title(self, title: str) -> BoardEntity | None:
        statement = select(BoardModel).where(BoardModel.title == title)

        db_board = self.db.scalar(statement)

        if not db_board:
            return None

        return to_entity(db_board, BoardEntity)

    def list_boards(self) -> list[BoardEntity]:
        statement = select(BoardModel)

        db_boards = list(self.db.scalars(statement).all())

        return to_entities(db_boards, BoardEntity)

    def add_board(self, new_board: NewBoard) -> BoardEntity:
        db_board = BoardModel(title=new_board.title)

        self.db.add(db_board)
        self.db.flush()
        self.db.refresh(db_board)

        return to_entity(db_board, BoardEntity)

    def update_board(self, board_patch: BoardPatch) -> BoardEntity:
        db_board = self.db.get(BoardModel, board_patch.id)

        if not db_board:
            raise BoardNotFoundException(board_patch.id)

        apply_patch_to_model(db_board, board_patch)

        self.db.commit()
        self.db.refresh(db_board)

        return to_entity(db_board, BoardEntity)

    def delete_board(self, board_id: int) -> None:
        db_board = self.db.get(BoardModel, board_id)

        if not db_board:
            raise BoardNotFoundException(board_id)

        self.db.delete(db_board)
        self.db.commit()
