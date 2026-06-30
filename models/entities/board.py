from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.associations.board_member import BoardMemberModel

    from .task import TaskModel


class BoardModel(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, insert_default=datetime.now, nullable=False
    )

    tasks: Mapped[list[TaskModel]] = relationship(back_populates="board")
    members: Mapped[list[BoardMemberModel]] = relationship(back_populates="boards")
