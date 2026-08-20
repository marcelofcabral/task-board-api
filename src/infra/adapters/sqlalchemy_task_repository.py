from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.task_repository_port import TaskRepositoryPort
from domain.entities.task_entity import TaskEntity
from infra.models import TaskModel


class SqlAlchemyTaskRepository(TaskRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, id: int) -> TaskEntity | None:
        db_task = self.db.get(TaskModel, id)

        if db_task is None:
            return None

        return TaskEntity(
            id=db_task.id,
            user_id=db_task.user_id,
            board_id=db_task.board_id,
            title=db_task.title,
            description=db_task.description,
            created_at=db_task.created_at,
        )

    def get_all_board_member_tasks(
        self, board_id: int, user_id: int
    ) -> list[TaskEntity]:
        statement = (
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .where(TaskModel.board_id == board_id)
        )

        db_tasks = list(self.db.scalars(statement).all())
        entities = []

        for db_task in db_tasks:
            entities.append(
                TaskEntity(
                    id=db_task.id,
                    user_id=db_task.user_id,
                    board_id=db_task.board_id,
                    title=db_task.title,
                    description=db_task.description,
                    created_at=db_task.created_at,
                )
            )

        return entities

    def get_all_board_tasks(self, board_id: int) -> list[TaskEntity]:
        statement = select(TaskModel).where(TaskModel.board_id == board_id)

        db_tasks = list(self.db.scalars(statement).all())
        entities = []

    def list_tasks(self) -> list[TaskEntity]: ...
    def create_task(self, task: TaskEntity) -> TaskEntity: ...
    def create_new_board_task(self, task: TaskEntity, board_id: int) -> TaskEntity: ...
    def update_task(self, task: TaskEntity) -> TaskEntity: ...
    def delete_task(self, task: TaskEntity) -> None: ...
