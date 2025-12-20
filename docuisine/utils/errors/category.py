from typing import Optional


class CategoryExistsError(Exception):
    """Exception raised when a category already exists."""

    def __init__(self, name: str):
        self.name = name
        self.message = f"Category with name '{self.name}' already exists."
        super().__init__(self.message)


class CategoryNotFoundError(Exception):
    """Exception raised when a category is not found."""

    def __init__(self, category_id: Optional[int] = None, name: Optional[str] = None):
        self.category_id = category_id
        self.name = name
        if name is not None:
            self.message = f"Category with name '{name}' not found."
        else:
            self.message = f"Category with ID {self.category_id} not found."
        super().__init__(self.message)
