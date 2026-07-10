from typing import Annotated

from fastapi import APIRouter, Depends, status

from deps.board_member import get_board_member_or_403
from deps.task import get_all_board_tasks, get_task_or_404, get_task_service
from models import TaskModel
from schemas import TaskCreate, TaskResponse, TaskUpdate
from services.task import TaskService

router = APIRouter(
    prefix="/{board_id}/tasks",
    dependencies=[Depends(get_board_member_or_403)],
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
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    board_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
):
    return service.create_board_task(task, board_id)


# Update board task
@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    task: Annotated[TaskModel, Depends(get_task_or_404)],
    updates: TaskUpdate,
    service: Annotated[TaskService, Depends(get_task_service)],
):
    return service.update_task(task, updates)


# Delete board task
@router.delete("/{id}")
async def delete_task(
    task: Annotated[TaskModel, Depends(get_task_or_404)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    return service.delete_task(task)
