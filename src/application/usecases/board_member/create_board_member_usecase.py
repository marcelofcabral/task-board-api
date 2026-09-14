from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from application.inputs.board_member.create_board_member_input import (
    CreateBoardMemberInput,
)
from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from application.ports.board_repository_port import BoardRepositoryPort
from application.ports.user_repository_port import UserRepositoryPort
from domain.entities.board_member_entity import BoardMemberEntity
from domain.exceptions.board import BoardNotFoundException
from domain.exceptions.board_member import BoardMemberAlreadyExistsException
from domain.exceptions.user import UserNotFoundException
from domain.value_objects.board_member.new_board_member import NewBoardMember
from infra.adapters.unit_of_work_adapter import UnitOfWorkAdapter


class CreateBoardMemberUsecase:
    def __init__(
        self,
        board_member_repo: BoardMemberRepositoryPort,
        board_repo: BoardRepositoryPort,
        user_repo: UserRepositoryPort,
        unit_of_work_adapter: UnitOfWorkAdapter,
    ) -> None:
        self.board_member_repo = board_member_repo
        self.board_repo = board_repo
        self.user_repo = user_repo
        self.unit_of_work_adapter = unit_of_work_adapter

    def _ensure_board_and_user_exist(self, board_id: int, user_id: int) -> None:
        board = self.board_repo.get_board(board_id)

        if not board:
            raise BoardNotFoundException(board_id)

        user = self.user_repo.get_user(user_id)

        if not user:
            raise UserNotFoundException(user_id)

    def _ensure_user_not_member_of_board(self, board_id: int, user_id: int) -> None:
        if self.board_member_repo.get_board_member(user_id, board_id) is not None:
            raise BoardMemberAlreadyExistsException(user_id, board_id)

    def execute(self, input: CreateBoardMemberInput) -> BoardMemberEntity:
        try:
            self._ensure_board_and_user_exist(input.board_id, input.user_id)
            self._ensure_user_not_member_of_board(input.board_id, input.user_id)
        except (BoardNotFoundException, UserNotFoundException) as exception:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=str(exception)
            ) from exception
        except BoardMemberAlreadyExistsException as exception:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT, detail=str(exception)
            ) from exception

        new_board_member = NewBoardMember(
            board_id=input.board_id, user_id=input.user_id, role=input.role
        )

        db_board_member = self.board_member_repo.add_board_member(new_board_member)
        self.unit_of_work_adapter.commit()

        return db_board_member
