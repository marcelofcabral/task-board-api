from models import TaskModel
from repositories import TaskRepository
from schemas import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_task(self, id: int) -> TaskModel | None:
        return self.repository.get_task(id)

    def get_all_board_member_tasks(
        self, board_id: int, board_member_id: int
    ) -> list[TaskModel]:
        return self.repository.get_all_board_member_tasks(board_id, board_member_id)

    def get_all_board_tasks(self, board_id: int) -> list[TaskModel]:
        return self.repository.get_all_board_tasks(board_id)

    def list_tasks(self) -> list[TaskModel]:
        return self.repository.list_tasks()

    def create_board_task(self, task: TaskCreate, board_id: int) -> TaskModel:
        return self.repository.create_board_task(task, board_id)

    def update_task(self, task: TaskModel, updates: TaskUpdate) -> TaskModel:
        return self.repository.update_task(task, updates)

    def delete_task(self, task: TaskModel) -> None:
        return self.repository.delete_task(task)
