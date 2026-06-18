from models import UserModel
from repositories import UserRepository
from schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, id: int) -> UserModel | None:
        return self.repository.get_user(id)

    def list_users(self) -> list[UserModel]:
        return self.repository.list_users()

    def create_user(self, user: UserCreate) -> UserModel:
        return self.repository.create_user(user)

    def update_user(self, user: UserModel, updates: UserUpdate) -> UserModel:
        return self.repository.update_user(user, updates)

    def delete_user(self, user: UserModel) -> None:
        return self.repository.delete_user(user)
