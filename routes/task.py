from typing import Annotated

from fastapi import APIRouter, Depends, status

from deps.auth import get_auth_user
from deps.task import get_all_tasks, get_task_or_404, get_task_service
from models import TaskModel
from schemas import TaskCreate, TaskResponse, TaskUpdate
from services.task import TaskService

router = APIRouter(
    prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_auth_user)]
)


# Read all tasks
@router.get("", response_model=list[TaskResponse])
async def read_all_tasks(
    tasks: Annotated[list[TaskModel], Depends(get_all_tasks)],
):
    return tasks


# Read task
@router.get("/{id}", response_model=TaskResponse)
async def read_task(task: Annotated[TaskModel, Depends(get_task_or_404)]):
    return task


# Create task
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate, service: Annotated[TaskService, Depends(get_task_service)]
):
    return service.create_task(task)


# Update task
@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    task: Annotated[TaskModel, Depends(get_task_or_404)],
    updates: TaskUpdate,
    service: Annotated[TaskService, Depends(get_task_service)],
):
    return service.update_task(task, updates)


# Delete task
@router.delete("/{id}")
async def delete_task(
    task: Annotated[TaskModel, Depends(get_task_or_404)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    return service.delete_task(task)
