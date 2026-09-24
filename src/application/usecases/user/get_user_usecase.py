from application.ports.user_repository_port import UserRepositoryPort
from domain.entities.user_entity import UserEntity


class GetUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(self, id: int) -> UserEntity | None:
        return self.user_repo.get_user(id)
