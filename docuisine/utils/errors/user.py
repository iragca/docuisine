from typing import Optional


class UserExistsError(Exception):
    """Exception raised when a user already exists."""

    def __init__(self, username: str):
        self.username = username
        self.message = f"User with username '{self.username}' already exists."
        super().__init__(self.message)


class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: Optional[int] = None, username: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        if username is not None:
            self.message = f"User with username '{username}' not found."
        else:
            self.message = f"User with ID {self.user_id} not found."
        super().__init__(self.message)


class DuplicateEmailError(Exception):
    """Exception raised when an email is already associated with another user."""

    def __init__(self, email: str):
        self.email = email
        self.message = f"Email '{self.email}' is already associated with another user."
        super().__init__(self.message)
