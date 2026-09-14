from application.ports.board_member_repository_port import BoardMemberRepositoryPort
from domain.entities.board_member_entity import BoardMemberEntity
from domain.exceptions.board_member import BoardMemberNotFoundException


class GetBoardMemberUsecase:
    def __init__(self, board_member_repo: BoardMemberRepositoryPort) -> None:
        self.board_member_repo = board_member_repo

    def execute(self, board_id: int, user_id: int) -> BoardMemberEntity:
        db_board_member = self.board_member_repo.get_board_member(board_id, user_id)

        if not db_board_member:
            raise BoardMemberNotFoundException(user_id, board_id)

        return db_board_member
