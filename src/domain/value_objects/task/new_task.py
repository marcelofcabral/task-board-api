from dataclasses import dataclass


@dataclass
class NewTask:
    title: str
    user_id: int
    board_id: int
    description: str | None = None
