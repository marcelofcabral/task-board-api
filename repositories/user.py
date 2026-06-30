from sqlalchemy import select
from sqlalchemy.orm import Session

from models import UserModel
from schemas import UserCreate
from schemas.user import UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, id: int) -> UserModel | None:
        return self.db.get(UserModel, id)

    def get_user_by_username(self, username: str) -> UserModel | None:
        return self.db.scalar(select(UserModel).where(UserModel.username == username))

    def list_users(self) -> list[UserModel]:
        return list(self.db.scalars(select(UserModel)).all())

    def create_user(self, user: UserCreate) -> UserModel:
        new_user = UserModel(**user.model_dump(exclude_unset=True))

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def update_user(self, user: UserModel, updates: UserUpdate) -> UserModel:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(self, user: UserModel) -> None:
        self.db.delete(user)
        self.db.commit()
