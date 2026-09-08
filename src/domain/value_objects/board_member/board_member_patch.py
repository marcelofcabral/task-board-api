from dataclasses import dataclass

from shared.types.board_member import BoardMemberRole


@dataclass
class BoardMemberPatch:
    id: int
    role: BoardMemberRole
