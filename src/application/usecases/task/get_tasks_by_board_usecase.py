from application.ports.task_repository_port import TaskRepositoryPort
from domain.entities.task_entity import TaskEntity


class GetTasksByBoardUsecase:
    def __init__(self, task_repo: TaskRepositoryPort) -> None:
        self.task_repo = task_repo

    def execute(self, board_id: int) -> list[TaskEntity]:
        return self.task_repo.get_all_board_tasks(board_id)
