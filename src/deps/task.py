from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.task_repository_port import TaskRepositoryPort
from application.usecases.task.create_board_task_usecase import CreateBoardTaskUseCase
from application.usecases.task.get_task_usecase import GetTaskUseCase
from application.usecases.task.get_tasks_by_board_usecase import GetTasksByBoardUsecase
from application.usecases.task.list_tasks_usecase import ListTasksUseCase
from database import get_db
from deps.board import get_authorized_board_or_404
from domain.entities.board_entity import BoardEntity
from domain.entities.task_entity import TaskEntity
from infra.adapters.sqlalchemy_task_repository import SqlAlchemyTaskRepository


def get_task_repository(db: Annotated[Session, Depends(get_db)]) -> TaskRepositoryPort:
    return SqlAlchemyTaskRepository(db)


def get_create_board_task_usecase(
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> CreateBoardTaskUseCase:
    return CreateBoardTaskUseCase(repository)


def get_get_task_usecase(
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> GetTaskUseCase:
    return GetTaskUseCase(repository)


def get_list_tasks_usecase(
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> ListTasksUseCase:
    return ListTasksUseCase(repository)


def get_get_tasks_by_board_usecase(
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> GetTasksByBoardUsecase:
    return GetTasksByBoardUsecase(repository)


def get_task_or_404(
    id: int, get_task_usecase: Annotated[GetTaskUseCase, Depends(get_get_task_usecase)]
) -> TaskEntity:
    task = get_task_usecase.execute(id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


def get_all_tasks(
    list_tasks_usecase: Annotated[ListTasksUseCase, Depends(get_list_tasks_usecase)],
) -> list[TaskEntity]:
    return list_tasks_usecase.execute()


def get_all_board_tasks(
    board: Annotated[BoardEntity, Depends(get_authorized_board_or_404)],
    get_tasks_by_board_usecase: Annotated[
        GetTasksByBoardUsecase, Depends(get_get_tasks_by_board_usecase)
    ],
) -> list[TaskEntity]:
    return get_tasks_by_board_usecase.execute(board.id)
