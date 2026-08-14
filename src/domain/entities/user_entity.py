from dataclasses import dataclass
from datetime import datetime

from .base_entity import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    username: str
    hashed_password: str
    birth: datetime
