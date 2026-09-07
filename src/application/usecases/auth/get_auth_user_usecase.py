import jwt

from application.ports.user_repository_port import UserRepositoryPort
from auth import ALGORITHM, SECRET_KEY
from domain.entities.user_entity import UserEntity
from domain.exceptions.auth import InvalidTokenException
from domain.exceptions.user import UserNotFoundException


class GetAuthUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(self, token: str) -> UserEntity:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str | None = payload.get("sub")

            if user_id is None:
                raise InvalidTokenException

            user = self.user_repo.get_user(int(user_id))

            if not user:
                raise UserNotFoundException

            return user

        except jwt.InvalidTokenError as exception:
            raise InvalidTokenException from exception
