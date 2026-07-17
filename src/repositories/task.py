from sqlalchemy import select
from sqlalchemy.orm import Session

from models import TaskModel
from schemas import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, id: int) -> TaskModel | None:
        return self.db.get(TaskModel, id)

    def get_all_board_member_tasks(
        self, board_id: int, board_member_id: int
    ) -> list[TaskModel]:
        return list(
            self.db.scalars(
                select(TaskModel)
                .where(TaskModel.board_id == board_id)
                .where(TaskModel.user_id == board_member_id)
            )
        )

    def get_all_board_tasks(self, board_id: int) -> list[TaskModel]:
        return list(
            self.db.scalars(select(TaskModel).where(TaskModel.board_id == board_id))
        )

    def list_tasks(self) -> list[TaskModel]:
        return list(self.db.scalars(select(TaskModel)).all())

    def create_task(self, task: TaskCreate) -> TaskModel:
        new_task = TaskModel(**task.model_dump())

        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

        return new_task

    def create_board_task(self, task: TaskCreate, board_id: int) -> TaskModel:
        new_task = TaskModel(**task.model_dump(), board_id=board_id)

        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

        return new_task

    def update_task(self, task: TaskModel, updates: TaskUpdate) -> TaskModel:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)

        return task

    def delete_task(self, task: TaskModel) -> None:
        self.db.delete(task)
        self.db.commit()
