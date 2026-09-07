from application.ports.task_repository_port import TaskRepositoryPort
from domain.entities.task_entity import TaskEntity
from domain.exceptions.task import TaskNotFoundException


class GetTaskUseCase:
    def __init__(self, task_repo: TaskRepositoryPort) -> None:
        self.task_repo = task_repo

    def execute(self, id: int) -> TaskEntity:
        task = self.task_repo.get_task(id)

        if task is None:
            raise TaskNotFoundException(id)

        return task
