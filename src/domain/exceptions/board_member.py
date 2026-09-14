class BoardMemberAlreadyExistsException(Exception):
    def __init__(self, user_id: int, board_id: int):
        self.user_id = user_id
        self.board_id = board_id
        super().__init__(
            f"Board member with user_id {user_id} and board {board_id} already exists"
        )


class BoardMemberNotFoundException(Exception):
    def __init__(self, user_id: int, board_id: int):
        self.user_id = user_id
        self.board_id = board_id
        super().__init__(
            f"Board member with user_id {user_id} and board {board_id} was not found"
        )
