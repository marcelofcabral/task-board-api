from application.ports.user_repository_port import UserRepositoryPort
from auth.utils import password_hasher
from domain.exceptions.user import UserAlreadyExistsException
from domain.value_objects.user.new_user import NewUser
from dtos.auth import RegistrationData


def get_hashed_password(password: str):
    return password_hasher.hash(password)


class RegisterUserUsecase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(self, registration_data: RegistrationData) -> None:
        user = self.user_repo.get_user_by_username(registration_data.username)

        if user:
            raise UserAlreadyExistsException(user.username)

        hashed_password = get_hashed_password(registration_data.password)

        self.user_repo.create_user(
            NewUser(
                username=registration_data.username,
                hashed_password=hashed_password,
                birth=registration_data.birth,
            )
        )
