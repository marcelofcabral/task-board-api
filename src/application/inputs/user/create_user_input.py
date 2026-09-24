from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateUserInput:
    username: str
    hashed_password: str
    birth: datetime
