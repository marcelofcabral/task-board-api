from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewUser:
    username: str
    hashed_password: str
    birth: datetime
