from typing import Annotated

from database import get_db
from fastapi import Depends, HTTPException, status
from models import TaskModel
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_task_or_404(id: int, db: Annotated[Session, Depends(get_db)]) -> TaskModel:
    task = db.get(TaskModel, id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


def get_all_tasks(db: Annotated[Session, Depends(get_db)]) -> list[TaskModel]:
    tasks = db.scalars(select(TaskModel)).all()

    return tasks
