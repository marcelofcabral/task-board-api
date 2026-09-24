class UserNotFoundException(Exception):
    def __init__(self, user_id: int | None = None):
        self.user_id = user_id
        super().__init__(
            f"User {user_id} not found" if user_id is not None else "User not found"
        )


class UserAlreadyExistsException(Exception):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f"User with {username} already exists")
