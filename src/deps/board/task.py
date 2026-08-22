from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.task_repository_port import TaskRepositoryPort
from application.use_cases.create_board_task import CreateBoardTaskUseCase
from database import get_db
from deps.board.board import get_authorized_board_or_404
from infra.adapters.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from models import BoardModel, TaskModel
from services import TaskService


def get_task_repository(db: Annotated[Session, Depends(get_db)]) -> TaskRepositoryPort:
    return SqlAlchemyTaskRepository(db)


def get_create_board_task_use_case(
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> CreateBoardTaskUseCase:
    return CreateBoardTaskUseCase(repository)


def get_task_or_404(
    id: int, service: Annotated[TaskService, Depends(get_task_service)]
) -> TaskModel:
    task = service.get_task(id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


def get_all_tasks(
    service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskModel]:
    return service.list_tasks()


def get_all_board_tasks(
    board: Annotated[BoardModel, Depends(get_authorized_board_or_404)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskModel]:
    return service.get_all_board_tasks(board.id)
