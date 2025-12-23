class InvalidCredentialsError(Exception):
    """Exception raised when provided credentials are invalid."""

    def __init__(self, message: str = "ICould not validate credentials."):
        self.message = message
        super().__init__(self.message)


class InvalidPasswordError(Exception):
    """Exception raised when a provided password is invalid."""

    def __init__(self, message: str = "The provided password is invalid."):
        self.message = message
        super().__init__(self.message)
