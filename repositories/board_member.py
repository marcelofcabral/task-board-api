from sqlalchemy import select
from sqlalchemy.orm import Session

from models import BoardMemberModel
from schemas import BoardMemberCreate
from shared.types.board_member import BoardMemberRole


class BoardMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_board_member(self, user_id: int, board_id: int) -> BoardMemberModel | None:
        return self.db.get(BoardMemberModel, {"user_id": user_id, "board_id": board_id})

    def list_board_members(self, board_id: int) -> list[BoardMemberModel]:
        return list(
            self.db.scalars(
                select(BoardMemberModel).where(BoardMemberModel.board_id == board_id)
            ).all()
        )

    def get_board_members_by_role(
        self, board_id: int, role: BoardMemberRole
    ) -> list[BoardMemberModel]:
        return list(
            self.db.scalars(
                select(BoardMemberModel).where(
                    BoardMemberModel.board_id == board_id, BoardMemberModel.role == role
                )
            )
        )

    def add_board_member(self, board_member: BoardMemberCreate) -> BoardMemberModel:
        new_board_member = BoardMemberModel(
            user_id=board_member.user_id,
            board_id=board_member.board_id,
            role=board_member.role,
        )

        self.db.add(new_board_member)

        return new_board_member

    def update_board_member(
        self, board_member: BoardMemberModel, new_role: BoardMemberRole
    ) -> BoardMemberModel:
        setattr(board_member, "role", new_role)

        self.db.commit()
        self.db.refresh(board_member)

        return board_member

    def delete_board_member(self, board_member: BoardMemberModel) -> None:
        self.db.delete(board_member)
        self.db.commit()
