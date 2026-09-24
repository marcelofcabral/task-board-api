from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserPatch:
    id: int
    username: str | None = None
    hashed_password: int | None = None
    birth: datetime | None = None
