from models import BoardModel
from repositories import BoardRepository
from schemas import BoardCreate, BoardMemberCreate, BoardUpdate
from shared.types.board_member import BoardMemberRole

from .board_member import BoardMemberService


class BoardService:
    def __init__(
        self, repository: BoardRepository, board_member_service: BoardMemberService
    ):
        self.repository = repository
        self.board_member_service = board_member_service

    def get_board(self, id: int) -> BoardModel | None:
        return self.repository.get_board(id)

    def list_boards(self) -> list[BoardModel]:
        return self.repository.list_boards()

    def create_board(self, board: BoardCreate, creator_id: int) -> BoardModel:
        new_board = self.repository.add_board(board)

        self.board_member_service.add_board_member(
            BoardMemberCreate(
                user_id=creator_id, board_id=new_board.id, role=BoardMemberRole.EDITOR
            )
        )

        # commits both changes to DB in a single transaction (db session is shared for the request)
        self.repository.commit()

        return new_board

    def update_board(self, board: BoardModel, updates: BoardUpdate) -> BoardModel:
        return self.repository.update_board(board, updates)

    def delete_board(self, board: BoardModel) -> None:
        return self.repository.delete_board(board)
