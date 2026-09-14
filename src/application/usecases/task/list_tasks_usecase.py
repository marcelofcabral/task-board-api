from application.ports.task_repository_port import TaskRepositoryPort
from domain.entities.task_entity import TaskEntity


class ListTasksUseCase:
    def __init__(self, task_repo: TaskRepositoryPort) -> None:
        self.task_repo = task_repo

    def execute(self) -> list[TaskEntity]:
        return self.task_repo.list_tasks()
