from typing import NamedTuple

from models import UserModel


class LoginResult(NamedTuple):
    user: UserModel
    token: str
