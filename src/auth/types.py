from typing import NamedTuple

from domain.entities.user_entity import UserEntity


class LoginResult(NamedTuple):
    user: UserEntity
    token: str
