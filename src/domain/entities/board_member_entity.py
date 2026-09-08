from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity
from shared.types.board_member import BoardMemberRole


@dataclass
class BoardMemberEntity(BaseEntity):
    user_id: int
    board_id: int
    role: BoardMemberRole
