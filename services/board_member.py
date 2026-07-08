from models import BoardMemberModel
from repositories import BoardMemberRepository
from schemas import BoardMemberCreate
from shared.types.board_member import BoardMemberRole


class BoardMemberService:
    def __init__(self, repository: BoardMemberRepository):
        self.repository = repository

    def get_board_member(self, user_id: int, board_id: int) -> BoardMemberModel | None:
        return self.repository.get_board_member(user_id, board_id)

    def list_board_members(self, board_id: int) -> list[BoardMemberModel]:
        return self.repository.list_board_members(board_id)

    def get_board_members_by_role(
        self, board_id: int, role: BoardMemberRole
    ) -> list[BoardMemberModel]:
        return self.repository.get_board_members_by_role(board_id, role)

    def add_board_member(self, board_member: BoardMemberCreate) -> BoardMemberModel:
        return self.repository.add_board_member(board_member)

    def update_board_member(
        self, board_member: BoardMemberModel, new_role: BoardMemberRole
    ) -> BoardMemberModel:
        return self.repository.update_board_member(board_member, new_role)

    def delete_board_member(self, board_member: BoardMemberModel) -> None:
        return self.repository.delete_board_member(board_member)
