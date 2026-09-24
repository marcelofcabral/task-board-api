from dataclasses import dataclass
from datetime import datetime


@dataclass
class UpdateUserInput:
    user_id: int
    username: str | None = None
    birth: datetime | None = None
