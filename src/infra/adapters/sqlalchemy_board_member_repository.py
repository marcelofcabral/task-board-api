from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from domain.entities.board_member_entity import BoardMemberEntity
from domain.exceptions.board_member import (
    BoardMemberNotFoundException,
)
from domain.value_objects.board_member.board_member_patch import BoardMemberPatch
from domain.value_objects.board_member.new_board_member import NewBoardMember
from infra.mappers.entity_mappers import to_entities, to_entity
from infra.models import BoardMemberModel
from shared.types.board_member import BoardMemberRole


class SqlAlchemyBoardMemberRepository(BoardMemberRepositoryPort):
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

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

    def add_board_member(self, new_board_member: NewBoardMember) -> BoardMemberEntity:
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
            raise BoardMemberNotFoundException(
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
            raise BoardMemberNotFoundException(user_id, board_id)

        self.db.delete(db_board_member)
        self.db.commit()
