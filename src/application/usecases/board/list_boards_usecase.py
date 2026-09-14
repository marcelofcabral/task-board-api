from application.ports.board_repository_port import BoardRepositoryPort
from domain.entities.board_entity import BoardEntity


class ListBoardsUseCase:
    def __init__(self, board_repo: BoardRepositoryPort) -> None:
        self.board_repo = board_repo

    def execute(self) -> list[BoardEntity]:
        boards = self.board_repo.list_boards()

        return boards
