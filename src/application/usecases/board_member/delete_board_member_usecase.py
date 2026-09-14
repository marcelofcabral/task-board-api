from application.ports.board_member_repository_port import BoardMemberRepositoryPort


class DeleteBoardMemberUsecase:
    def __init__(self, board_member_repo: BoardMemberRepositoryPort) -> None:
        self.board_member_repo = board_member_repo

    def execute(self, board_id: int, user_id: int) -> None:
        self.board_member_repo.delete_board_member(user_id, board_id)
