import store
from deps.tasks import get_task_or_404
from fastapi import APIRouter, Depends
from models import Task, TaskDTO

router = APIRouter(prefix="/task", tags=["Tasks"])


# Read all task
@router.get("")
async def read_all_tasks():
    return store.tasks


# Read task
@router.get("/{id}")
async def read_task(task=Depends(get_task_or_404)):
    return task


# Create task
@router.post("")
async def create_task(task: TaskDTO):
    new_task = Task(**task.model_dump(), id=store.next_task_id)
    store.tasks[store.next_task_id] = new_task

    store.next_task_id = store.next_task_id + 1

    return new_task


# Update task
@router.put("/{id}")
async def update_task(id: int, task: Task, _=Depends(get_task_or_404)):
    store.tasks[id] = task

    return task


# Delete task
@router.delete("/{id}")
async def delete_task(id: int, _=Depends(get_task_or_404)):
    task = store.tasks[id]
    del store.tasks[id]

    return task
