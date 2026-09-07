from application.inputs.board.create_board_input import CreateBoardInput
from application.ports.board_repository_port import BoardRepositoryPort
from domain.entities.board_entity import BoardEntity
from domain.value_objects.board.new_board import NewBoard


class CreateBoardUseCase:
    def __init__(self, board_repo: BoardRepositoryPort) -> None:
        self.board_repo = board_repo

    def execute(self, input: CreateBoardInput) -> BoardEntity:
        new_board_vo = NewBoard(title=input.title)

        return self.board_repo.create_board(new_board_vo)
