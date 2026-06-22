from models import BoardModel
from repositories import BoardRepository
from schemas import BoardCreate, BoardUpdate


class BoardService:
    def __init__(self, repository: BoardRepository):
        self.repository = repository

    # Basic CRUD
    def get_board(self, id: int) -> BoardModel | None:
        return self.repository.get_board(id)

    def list_boards(self) -> list[BoardModel]:
        return self.repository.list_boards()

    def create_board(self, board: BoardCreate) -> BoardModel:
        return self.repository.create_board(board)

    def update_board(self, board: BoardModel, updates: BoardUpdate) -> BoardModel:
        return self.repository.update_board(board, updates)

    def delete_board(self, board: BoardModel) -> None:
        return self.repository.delete_board(board)
