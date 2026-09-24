class UserCredentialsIncorrectException(Exception):
    def __init__(self):
        super().__init__("User credentials incorrect. Please try again.")


class InvalidTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid token")
