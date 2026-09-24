from application.inputs.task.update_board_task_input import UpdateBoardTaskInput
from application.ports.task_repository_port import TaskRepositoryPort
from domain.entities.task_entity import TaskEntity
from domain.value_objects.task.task_patch import TaskPatch


class UpdateBoardTaskUseCase:
    def __init__(self, task_repo: TaskRepositoryPort) -> None:
        self.task_repo = task_repo

    def execute(self, input: UpdateBoardTaskInput) -> TaskEntity:
        task_patch = TaskPatch(
            id=input.task_id,
            board_id=input.board_id,
            description=input.description,
            title=input.title,
            user_id=input.user_id,
        )

        return self.task_repo.update_task(task_patch)
