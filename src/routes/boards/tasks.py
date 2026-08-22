from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.inputs.create_board_task_input import CreateBoardTaskInput
from application.use_cases.create_board_task import CreateBoardTaskUseCase
from deps.board.member import (
    get_auth_board_member_or_403,
    require_board_member_editor_role,
)
from deps.board.task import (
    get_all_board_tasks,
    get_create_board_task_use_case,
    get_task_or_404,
    get_task_service,
)
from dtos import TaskCreate, TaskResponse, TaskUpdate
from models import TaskModel
from services.task import TaskService

router = APIRouter(
    prefix="/{board_id}/tasks",
    dependencies=[Depends(get_auth_board_member_or_403)],
)


# Read all board tasks
@router.get("", response_model=list[TaskResponse])
async def read_all_board_tasks(
    tasks: Annotated[list[TaskModel], Depends(get_all_board_tasks)],
):
    return tasks


# Read a board task
@router.get("/{id}", response_model=TaskResponse)
async def read_board_task(task: Annotated[TaskModel, Depends(get_task_or_404)]):
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
    input = CreateBoardTaskInput(**creation_dto.model_dump(), board_id=board_id)

    return use_case.execute(input)


# Update board task
@router.put(
    "/{id}",
    response_model=TaskResponse,
    dependencies=[Depends(require_board_member_editor_role)],
)
async def update_task(
    task: Annotated[TaskModel, Depends(get_task_or_404)],
    updates: TaskUpdate,
    service: Annotated[TaskService, Depends(get_task_service)],
):
    return service.update_task(task, updates)


# Delete board task
@router.delete("/{id}", dependencies=[Depends(require_board_member_editor_role)])
async def delete_task(
    task: Annotated[TaskModel, Depends(get_task_or_404)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    return service.delete_task(task)
