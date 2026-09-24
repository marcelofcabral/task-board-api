from application.ports.board_repository_port import BoardRepositoryPort
from domain.entities.board_entity import BoardEntity
from domain.exceptions.board import BoardNotFoundException


class GetBoardUseCase:
    def __init__(self, board_repo: BoardRepositoryPort) -> None:
        self.board_repo = board_repo

    def execute(self, id: int) -> BoardEntity:
        board = self.board_repo.get_board(id)

        if board is None:
            raise BoardNotFoundException(id)

        return board
