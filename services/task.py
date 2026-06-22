from models import TaskModel
from repositories import TaskRepository
from schemas import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    # Basic CRUD
    def get_task(self, id: int) -> TaskModel | None:
        return self.repository.get_task(id)

    def list_tasks(self) -> list[TaskModel]:
        return self.repository.list_tasks()

    def create_task(self, task: TaskCreate) -> TaskModel:
        return self.repository.create_task(task)

    def update_task(self, task: TaskModel, updates: TaskUpdate) -> TaskModel:
        return self.repository.update_task(task, updates)

    def delete_task(self, task: TaskModel) -> None:
        return self.repository.delete_task(task)
