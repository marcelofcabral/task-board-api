from application.ports.user_repository_port import UserRepositoryPort


class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(self, user_id: int) -> None:
        self.user_repo.delete_user(user_id)
