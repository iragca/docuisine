from fastapi import HTTPException, status


class InvalidCredentialsError(Exception):
    """Exception raised when provided credentials are invalid."""

    def __init__(self, message: str = "Could not validate credentials."):
        self.message = message
        super().__init__(self.message)


class InvalidPasswordError(Exception):
    """Exception raised when a provided password is invalid."""

    def __init__(self, message: str = "The provided password is invalid."):
        self.message = message
        super().__init__(self.message)


ForbiddenAccessError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to perform this action.",
)
