from application.inputs.create_board_task_input import CreateBoardTaskInput
from application.ports.task_repository_port import TaskRepositoryPort
from domain.entities.task_entity import TaskEntity
from domain.value_objects.task.new_task import NewTask


class CreateBoardTaskUseCase:
    def __init__(self, task_repo: TaskRepositoryPort):
        self.task_repo = task_repo

    def execute(self, input: CreateBoardTaskInput) -> TaskEntity:
        new_task_vo = NewTask(
            board_id=input.board_id,
            user_id=input.user_id,
            title=input.title,
            description=input.description,
        )

        return self.task_repo.create_board_task(new_task_vo)
