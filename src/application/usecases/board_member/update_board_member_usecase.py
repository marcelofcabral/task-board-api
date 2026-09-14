from application.inputs.board_member.update_board_member_input import (
    UpdateBoardMemberInput,
)
from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from domain.entities.board_member_entity import BoardMemberEntity
from domain.value_objects.board_member.board_member_patch import BoardMemberPatch


class UpdateBoardMemberUsecase:
    def __init__(
        self,
        board_member_repo: BoardMemberRepositoryPort,
    ) -> None:
        self.board_member_repo = board_member_repo

    def execute(self, input: UpdateBoardMemberInput) -> BoardMemberEntity:
        board_member_patch = BoardMemberPatch(
            board_id=input.board_id, user_id=input.user_id, role=input.role
        )

        return self.board_member_repo.update_board_member(board_member_patch)
