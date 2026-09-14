from application.ports.user_repository_port import UserRepositoryPort
from domain.entities.user_entity import UserEntity
from domain.exceptions.user import UserNotFoundException


class GetUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(self, id: int) -> UserEntity:
        user = self.user_repo.get_user(id)

        if not user:
            raise UserNotFoundException(id)

        return user
