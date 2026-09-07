class BoardNotFoundException(Exception):
    def __init__(self, board_id: int) -> None:
        self.board_id = board_id
        super().__init__(f"Board {board_id} not found")
