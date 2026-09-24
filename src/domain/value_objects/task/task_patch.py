from dataclasses import dataclass


@dataclass
class TaskPatch:
    id: int
    title: str | None = None
    user_id: int | None = None
    board_id: int | None = None
    description: str | None = None
