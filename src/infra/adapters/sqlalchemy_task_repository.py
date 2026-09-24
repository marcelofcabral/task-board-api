from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.task_repository_port import TaskRepositoryPort
from domain.entities.task_entity import TaskEntity
from domain.exceptions.task import TaskNotFoundException
from domain.value_objects.task.new_task import NewTask
from domain.value_objects.task.task_patch import TaskPatch
from infra.mappers.entity_mappers import to_entities, to_entity
from infra.mappers.model_mappers import apply_patch_to_model, to_model
from infra.models import TaskModel


class SqlAlchemyTaskRepository(TaskRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, id: int) -> TaskEntity | None:
        db_task = self.db.get(TaskModel, id)

        if db_task is None:
            return None

        return to_entity(db_task, TaskEntity)

    def get_all_board_member_tasks(
        self, board_id: int, user_id: int
    ) -> list[TaskEntity]:
        statement = (
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .where(TaskModel.board_id == board_id)
        )

        db_tasks = list(self.db.scalars(statement).all())

        return to_entities(db_tasks, TaskEntity)

    def get_all_board_tasks(self, board_id: int) -> list[TaskEntity]:
        statement = select(TaskModel).where(TaskModel.board_id == board_id)

        db_tasks = list(self.db.scalars(statement).all())

        return to_entities(db_tasks, TaskEntity)

    def list_tasks(self) -> list[TaskEntity]:
        statement = select(TaskModel)

        db_tasks = list(self.db.scalars(statement).all())

        return to_entities(db_tasks, TaskEntity)

    def create_board_task(self, new_task: NewTask) -> TaskEntity:
        new_db_task = to_model(new_task, TaskModel)

        self.db.add(new_db_task)
        self.db.commit()
        self.db.refresh(new_db_task)

        return to_entity(new_db_task, TaskEntity)

    def update_task(self, task_patch: TaskPatch) -> TaskEntity:
        db_task = self.db.get(TaskModel, task_patch.id)

        if not db_task:
            raise TaskNotFoundException(task_patch.id)

        apply_patch_to_model(db_task, task_patch)

        self.db.commit()
        self.db.refresh(db_task)

        return to_entity(db_task, TaskEntity)

    def delete_task(self, task_id: int) -> None:
        db_task = self.db.get(TaskModel, task_id)

        if not db_task:
            raise TaskNotFoundException(task_id)

        self.db.delete(db_task)
        self.db.commit()
