from dataclasses import dataclass


@dataclass
class CreateBoardTaskInput:
    board_id: int
    user_id: int
    title: str
    description: str | None = None
