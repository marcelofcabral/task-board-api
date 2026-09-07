from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.user_repository_port import UserRepositoryPort
from domain.entities.user_entity import UserEntity
from domain.exceptions.user import UserNotFoundException
from domain.value_objects.user.new_user import NewUser
from domain.value_objects.user.user_patch import UserPatch
from infra.mappers.entity_mappers import to_entities, to_entity
from infra.mappers.model_mappers import apply_patch_to_model
from models import UserModel


class SqlAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user(self, id: int) -> UserEntity | None:
        db_user = self.db.get(UserModel, id)

        if not db_user:
            return None

        return to_entity(db_user, UserEntity)

    def get_user_by_username(self, username: str) -> UserEntity | None:
        statement = select(UserModel).where(UserModel.username == username)

        db_user = self.db.scalar(statement)

        if not db_user:
            return None

        return to_entity(db_user, UserEntity)

    def get_users_by_ids(self, ids: list[int]) -> list[UserEntity]:
        statement = select(UserModel).where(UserModel.id.in_(ids))

        db_users = list(self.db.scalars(statement).all())

        return to_entities(db_users, UserEntity)

    def list_users(self) -> list[UserEntity]:
        statement = select(UserModel)

        db_users = list(self.db.scalars(statement).all())

        return to_entities(db_users, UserEntity)

    def create_user(self, new_user: NewUser) -> UserEntity:
        new_db_user = UserModel(
            username=new_user.username,
            birth=new_user.birth,
            hashed_password=new_user.hashed_password,
        )

        self.db.add(new_db_user)
        self.db.commit()
        self.db.refresh(new_db_user)

        return to_entity(new_db_user, UserEntity)

    def update_user(self, user_patch: UserPatch) -> UserEntity | None:
        db_user = self.db.get(UserModel, user_patch.id)

        if not db_user:
            raise UserNotFoundException(user_patch.id)

        apply_patch_to_model(db_user, user_patch)

        self.db.commit()
        self.db.refresh(db_user)

        return to_entity(db_user, UserEntity)

    def delete_user(self, user_id: int) -> None:
        db_user = self.db.get(UserModel, user_id)

        if not db_user:
            raise UserNotFoundException(user_id)

        self.db.delete(db_user)
        self.db.commit()
