from models import UserModel
from repositories import UserRepository
from schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    # Basic CRUD
    def get_user(self, id: int) -> UserModel | None:
        return self.repository.get_user(id)

    def get_user_by_username(self, username: str) -> UserModel | None:
        return self.repository.get_user_by_username(username)

    def get_users_by_ids(self, ids: list[int]) -> list[UserModel]:
        return self.repository.get_users_by_ids(ids)

    def list_users(self) -> list[UserModel]:
        return self.repository.list_users()

    def create_user(self, user: UserCreate) -> UserModel:
        return self.repository.create_user(user)

    def update_user(self, user: UserModel, updates: UserUpdate) -> UserModel:
        return self.repository.update_user(user, updates)

    def delete_user(self, user: UserModel) -> None:
        return self.repository.delete_user(user)
