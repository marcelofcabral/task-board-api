from dataclasses import dataclass


@dataclass
class CreateBoardInput:
    creator_id: int
    title: str
