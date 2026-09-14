from application.ports.board_repository_port import BoardRepositoryPort


class DeleteBoardUseCase:
    def __init__(self, board_repo: BoardRepositoryPort) -> None:
        self.board_repo = board_repo

    def execute(self, board_id: int) -> None:
        self.board_repo.delete_board(board_id)
