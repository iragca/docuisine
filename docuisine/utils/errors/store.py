from typing import Optional


class StoreExistsError(Exception):
    """Exception raised when a store already exists."""

    def __init__(self, name: str):
        self.name = name
        self.message = f"Store with name '{self.name}' already exists."
        super().__init__(self.message)


class StoreNotFoundError(Exception):
    """Exception raised when a store is not found."""

    def __init__(self, store_id: Optional[int] = None, name: Optional[str] = None):
        self.store_id = store_id
        self.name = name
        if name is not None:
            self.message = f"Store with name '{name}' not found."
        else:
            self.message = f"Store with ID {self.store_id} not found."
        super().__init__(self.message)
