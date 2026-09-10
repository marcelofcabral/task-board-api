from application.inputs.board.create_board_input import CreateBoardInput
from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from application.ports.board_repository_port import BoardRepositoryPort
from application.ports.unit_of_work_port import UnitOfWorkPort
from domain.entities.board_entity import BoardEntity
from domain.value_objects.board.new_board import NewBoard
from domain.value_objects.board_member.new_board_member import NewBoardMember
from shared.types.board_member import BoardMemberRole


class CreateBoardUseCase:
    def __init__(
        self,
        board_repo: BoardRepositoryPort,
        board_member_repo: BoardMemberRepositoryPort,
        unit_of_work_adapter: UnitOfWorkPort,
    ) -> None:
        self.board_repo = board_repo
        self.board_member_repo = board_member_repo
        self.unit_of_work_adapter = unit_of_work_adapter

    def execute(self, input: CreateBoardInput) -> BoardEntity:
        new_board_vo = NewBoard(title=input.title)
        new_board = self.board_repo.add_board(new_board_vo)

        new_board_member_vo = NewBoardMember(
            board_id=new_board.id, user_id=input.creator_id, role=BoardMemberRole.EDITOR
        )
        self.board_member_repo.add_board_member(new_board_member_vo)

        self.unit_of_work_adapter.commit()

        return new_board
