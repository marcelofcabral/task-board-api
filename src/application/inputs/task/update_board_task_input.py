from dataclasses import dataclass


@dataclass
class UpdateBoardTaskInput:
    task_id: int
    user_id: int | None = None
    title: str | None = None
    board_id: int | None = None
    description: str | None = None
