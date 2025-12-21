from typing import Optional


class RecipeExistsError(Exception):
    """Exception raised when a recipe already exists."""

    def __init__(self, name: str):
        self.name = name
        self.message = f"Recipe with name '{self.name}' already exists."
        super().__init__(self.message)


class RecipeNotFoundError(Exception):
    """Exception raised when a recipe is not found."""

    def __init__(self, recipe_id: Optional[int] = None, name: Optional[str] = None):
        self.recipe_id = recipe_id
        self.name = name
        if name is not None:
            self.message = f"Recipe with name '{name}' not found."
        else:
            self.message = f"Recipe with ID {self.recipe_id} not found."
        super().__init__(self.message)
