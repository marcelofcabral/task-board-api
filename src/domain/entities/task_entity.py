from dataclasses import dataclass

from .base_entity import BaseEntity


@dataclass
class TaskEntity(BaseEntity):
    user_id: int
    board_id: int
    title: str
    description: str | None = None
