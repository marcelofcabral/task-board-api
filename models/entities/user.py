from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.associations.board_member import BoardMemberModel

if TYPE_CHECKING:
    from .task import TaskModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, insert_default=datetime.now, nullable=False
    )

    tasks: Mapped[list[TaskModel]] = relationship(back_populates="user")
    memberships: Mapped[list[BoardMemberModel]] = relationship(back_populates="users")
