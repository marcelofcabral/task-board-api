from dataclasses import dataclass


@dataclass
class UpdateBoardInput:
    board_id: int
    title: str
