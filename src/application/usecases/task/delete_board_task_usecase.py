from application.ports.task_repository_port import TaskRepositoryPort


class DeleteBoardTaskUseCase:
    def __init__(self, task_repo: TaskRepositoryPort) -> None:
        self.task_repo = task_repo

    def execute(self, task_id: int) -> None:
        self.task_repo.delete_task(task_id)
