from datetime import datetime

from database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, insert_default=datetime.now, nullable=False
    )

    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="user")


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, insert_default=datetime.now, nullable=False
    )

    user: Mapped["UserModel"] = relationship(back_populates="tasks")
    board: Mapped["BoardModel"] = relationship(back_populates="tasks")


class BoardModel(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, insert_default=datetime.now, nullable=False
    )

    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="board")
