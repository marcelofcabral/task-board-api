from application.inputs.user.create_user_input import CreateUserInput
from application.ports.user_repository_port import UserRepositoryPort
from domain.entities.user_entity import UserEntity
from domain.value_objects.user.new_user import NewUser


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(self, input: CreateUserInput) -> UserEntity:
        return self.user_repo.create_user(
            NewUser(
                username=input.username,
                hashed_password=input.hashed_password,
                birth=input.birth,
            )
        )
