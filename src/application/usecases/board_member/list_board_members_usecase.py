from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from domain.entities.board_member_entity import BoardMemberEntity


class ListBoardMembersUsecase:
    def __init__(self, board_member_repo: BoardMemberRepositoryPort) -> None:
        self.board_member_repo = board_member_repo

    def execute(self, board_id: int) -> list[BoardMemberEntity]:
        return self.board_member_repo.list_board_members(board_id)
