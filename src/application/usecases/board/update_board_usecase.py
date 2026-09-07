from application.inputs.board.update_board_input import UpdateBoardInput
from application.ports.board_repository_port import BoardRepositoryPort
from domain.value_objects.board.board_patch import BoardPatch


class UpdateBoardUseCase:
    def __init__(self, board_repo: BoardRepositoryPort) -> None:
        self.board_repo = board_repo

    def execute(self, input: UpdateBoardInput):
        board_patch_vo = BoardPatch(id=input.board_id, title=input.title)

        return self.board_repo.update_board(board_patch_vo)
