from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from shared.types.board_member import BoardMemberRole

if TYPE_CHECKING:
    from models.entities.board import BoardModel
    from models.entities.user import UserModel


class BoardMemberModel(Base):
    __tablename__ = "board_members"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    board_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("boards.id"), primary_key=True
    )
    role: Mapped[BoardMemberRole] = mapped_column(String, nullable=False)

    users: Mapped[list[UserModel]] = relationship(back_populates="memberships")
    boards: Mapped[list[BoardModel]] = relationship(back_populates="members")
