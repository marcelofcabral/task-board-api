from application.inputs.user.update_user_input import UpdateUserInput
from application.ports.user_repository_port import UserRepositoryPort
from domain.entities.user_entity import UserEntity
from domain.value_objects.user.user_patch import UserPatch


class UpdateUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(self, input: UpdateUserInput) -> UserEntity:
        return self.user_repo.update_user(
            UserPatch(id=input.user_id, username=input.username, birth=input.birth)
        )
