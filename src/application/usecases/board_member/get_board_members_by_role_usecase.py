from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from domain.entities.board_member_entity import BoardMemberEntity
from shared.types.board_member import BoardMemberRole


class GetBoardMembersByRoleUsecase:
    def __init__(self, board_member_repo: BoardMemberRepositoryPort) -> None:
        self.board_member_repo = board_member_repo

    def execute(self, board_id: int, role: BoardMemberRole) -> list[BoardMemberEntity]:
        return self.board_member_repo.get_board_members_by_role(board_id, role)
