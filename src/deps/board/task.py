from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.ports.task_repository_port import TaskRepositoryPort
from application.usecases.task.create_board_task_usecase import CreateBoardTaskUseCase
from application.usecases.task.get_task_usecase import GetTaskUseCase
from application.usecases.task.update_board_task_usecase import UpdateBoardTaskUseCase
from database import get_db
from deps.board.board import get_authorized_board_or_404
from domain.entities.board_entity import BoardEntity
from domain.entities.task_entity import TaskEntity
from domain.exceptions.task import TaskNotFoundException
from infra.adapters.sqlalchemy_task_repository import SqlAlchemyTaskRepository


def get_task_repository(db: Annotated[Session, Depends(get_db)]) -> TaskRepositoryPort:
    return SqlAlchemyTaskRepository(db)


def get_create_board_task_use_case(
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> CreateBoardTaskUseCase:
    return CreateBoardTaskUseCase(repository)


def get_get_task_use_case(
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> GetTaskUseCase:
    return GetTaskUseCase(repository)


def get_update_board_task_use_case(
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> UpdateBoardTaskUseCase:
    return UpdateBoardTaskUseCase(repository)


def get_task_or_404(
    id: int,
    get_task_usecase: Annotated[GetTaskUseCase, Depends(get_get_task_use_case)],
) -> TaskEntity:
    try:
        return get_task_usecase.execute(id)
    except TaskNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        ) from exception


def get_all_board_tasks(
    board: Annotated[BoardEntity, Depends(get_authorized_board_or_404)],
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
) -> list[TaskEntity]:
    return repository.get_all_board_tasks(board.id)
