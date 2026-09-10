from dataclasses import dataclass

from shared.types.board_member import BoardMemberRole


@dataclass
class BoardMemberPatch:
    user_id: int
    board_id: int
    role: BoardMemberRole
