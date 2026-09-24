from abc import ABC

from domain.entities.board_member_entity import BoardMemberEntity
from domain.value_objects.board_member.board_member_patch import BoardMemberPatch
from domain.value_objects.board_member.new_board_member import NewBoardMember
from shared.types.board_member import BoardMemberRole


class BoardMemberRepositoryPort(ABC):
    def get_board_member(
        self, user_id: int, board_id: int
    ) -> BoardMemberEntity | None: ...

    def list_board_members(self, board_id: int) -> list[BoardMemberEntity]: ...

    def get_board_members_by_role(
        self, board_id: int, role: BoardMemberRole
    ) -> list[BoardMemberEntity]: ...

    # does not commit. Used by CreateBoardUseCase when creating a board and adding the creator as editor
    def add_board_member(
        self, new_board_member: NewBoardMember
    ) -> BoardMemberEntity: ...

    def update_board_member(
        self, board_member_patch: BoardMemberPatch
    ) -> BoardMemberEntity: ...

    def delete_board_member(self, user_id: int, board_id: int) -> None: ...
