from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps.board import get_authorized_board_or_404
from models import BoardModel, TaskModel
from repositories import TaskRepository
from services import TaskService


def get_task_repository(db: Annotated[Session, Depends(get_db)]) -> TaskRepository:
    return TaskRepository(db)


def get_task_service(
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
) -> TaskService:
    return TaskService(repository)


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
