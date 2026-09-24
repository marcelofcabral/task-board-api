from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.inputs.task.create_board_task_input import CreateBoardTaskInput
from application.inputs.task.update_board_task_input import UpdateBoardTaskInput
from application.ports.task_repository_port import TaskRepositoryPort
from application.usecases.task.create_board_task_usecase import CreateBoardTaskUseCase
from application.usecases.task.update_board_task_usecase import UpdateBoardTaskUseCase
from deps.board.member import (
    get_auth_board_member_or_403,
    require_board_member_editor_role,
)
from deps.board.task import (
    get_all_board_tasks,
    get_create_board_task_use_case,
    get_task_or_404,
    get_task_repository,
    get_update_board_task_use_case,
)
from domain.entities.task_entity import TaskEntity
from dtos import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(
    prefix="/{board_id}/tasks",
    dependencies=[Depends(get_auth_board_member_or_403)],
)


# Read all board tasks
@router.get("", response_model=list[TaskResponse])
async def read_all_board_tasks(
    tasks: Annotated[list[TaskEntity], Depends(get_all_board_tasks)],
):
    return tasks


# Read a board task
@router.get("/{id}", response_model=TaskResponse)
async def read_board_task(task: Annotated[TaskEntity, Depends(get_task_or_404)]):
    return task


# Create board task
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_board_member_editor_role)],
)
async def create_task(
    creation_dto: TaskCreate,
    board_id: int,
    use_case: Annotated[
        CreateBoardTaskUseCase, Depends(get_create_board_task_use_case)
    ],
):
    return use_case.execute(
        CreateBoardTaskInput(**creation_dto.model_dump(), board_id=board_id)
    )


# Update board task
@router.put(
    "/{id}",
    response_model=TaskResponse,
    dependencies=[Depends(require_board_member_editor_role)],
)
async def update_task(
    task: Annotated[TaskEntity, Depends(get_task_or_404)],
    updates: TaskUpdate,
    update_board_task_usecase: Annotated[
        UpdateBoardTaskUseCase, Depends(get_update_board_task_use_case)
    ],
):
    return update_board_task_usecase.execute(
        UpdateBoardTaskInput(
            task_id=task.id,
            user_id=updates.user_id,
            title=updates.title,
            board_id=task.board_id,
            description=updates.description,
        )
    )


# Delete board task
@router.delete("/{id}", dependencies=[Depends(require_board_member_editor_role)])
async def delete_task(
    task: Annotated[TaskEntity, Depends(get_task_or_404)],
    repository: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
):
    return repository.delete_task(task.id)
