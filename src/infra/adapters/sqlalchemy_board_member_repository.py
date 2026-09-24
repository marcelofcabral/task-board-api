from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from application.ports.board_repository_port import BoardRepositoryPort
from application.ports.user_repository_port import UserRepositoryPort
from domain.entities.board_member_entity import BoardMemberEntity
from domain.exceptions.board import BoardNotFoundException
from domain.exceptions.board_member import (
    BoardMemberAlreadyExistsException,
    BoardMemberNotFound,
)
from domain.exceptions.user import UserNotFoundException
from domain.value_objects.board_member.board_member_patch import BoardMemberPatch
from domain.value_objects.board_member.new_board_member import NewBoardMember
from infra.mappers.entity_mappers import to_entities, to_entity
from infra.models import BoardMemberModel
from shared.types.board_member import BoardMemberRole


class BoardMemberRepository(BoardMemberRepositoryPort):
    def __init__(
        self,
        db: Session,
        user_repo: UserRepositoryPort,
        board_repo: BoardRepositoryPort,
    ) -> None:
        self.db = db
        self.user_repo = user_repo
        self.board_repo = board_repo

    def get_board_member(self, user_id: int, board_id: int) -> BoardMemberEntity | None:
        db_board_member = self.db.get(
            BoardMemberModel, {"user_id": user_id, "board_id": board_id}
        )

        if not db_board_member:
            return None

        return to_entity(db_board_member, BoardMemberEntity)

    def list_board_members(self, board_id: int) -> list[BoardMemberEntity]:
        statement = select(BoardMemberModel).where(
            BoardMemberModel.board_id == board_id
        )

        db_board_members = list(self.db.scalars(statement).all())

        return to_entities(db_board_members, BoardMemberEntity)

    def get_board_members_by_role(
        self, board_id: int, role: BoardMemberRole
    ) -> list[BoardMemberEntity]:
        statement = select(BoardMemberModel).where(
            BoardMemberModel.board_id == board_id, BoardMemberModel.role == role
        )

        db_board_members = list(self.db.scalars(statement).all())

        return to_entities(db_board_members, BoardMemberEntity)

    def _ensure_board_and_user_exist(self, board_id: int, user_id: int) -> None:
        board = self.board_repo.get_board(board_id)

        if not board:
            raise BoardNotFoundException(board_id)

        user = self.user_repo.get_user(user_id)

        if not user:
            raise UserNotFoundException(user_id)

    def _ensure_user_not_member_of_board(self, board_id: int, user_id: int) -> None:
        if self.get_board_member(user_id, board_id) is not None:
            raise BoardMemberAlreadyExistsException(user_id, board_id)

    def add_board_member(self, new_board_member: NewBoardMember) -> BoardMemberEntity:
        self._ensure_board_and_user_exist(
            new_board_member.board_id, new_board_member.user_id
        )

        self._ensure_user_not_member_of_board(
            new_board_member.board_id, new_board_member.user_id
        )

        new_db_board_member = BoardMemberModel(
            board_id=new_board_member.board_id,
            user_id=new_board_member.user_id,
            role=new_board_member.role,
        )

        self.db.add(new_db_board_member)
        self.db.flush()
        self.db.refresh(new_db_board_member)

        return to_entity(new_db_board_member, BoardMemberEntity)

    def update_board_member(
        self, board_member_patch: BoardMemberPatch
    ) -> BoardMemberEntity:
        db_board_member = self.db.get(
            BoardMemberModel,
            {
                "user_id": board_member_patch.user_id,
                "board_id": board_member_patch.board_id,
            },
        )

        if not db_board_member:
            raise BoardMemberNotFound(
                board_member_patch.user_id, board_member_patch.board_id
            )

        db_board_member.role = board_member_patch.role

        self.db.commit()

        return to_entity(db_board_member, BoardMemberEntity)

    def delete_board_member(self, user_id: int, board_id: int) -> None:
        db_board_member = self.db.get(
            BoardMemberModel,
            {
                "user_id": user_id,
                "board_id": board_id,
            },
        )

        if not db_board_member:
            raise BoardMemberNotFound(user_id, board_id)

        self.db.delete(db_board_member)
