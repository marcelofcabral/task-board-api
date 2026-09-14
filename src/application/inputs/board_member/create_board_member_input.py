from dataclasses import dataclass

from shared.types.board_member import BoardMemberRole


@dataclass
class CreateBoardMemberInput:
    board_id: int
    user_id: int
    role: BoardMemberRole
