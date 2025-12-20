from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, Entity


class Category(Base, Entity):
    """
    Category model representing a category of recipes.
    E.g., "Dessert", "Vegetarian", "Korean", etc.

    Attributes
    ----------
    id : int
        Primary key identifier for the category.
    name : str
        Name of the category.
    description : Optional[str]
        Description of the category.
    recipes : List[Recipe]
        Recipes that belong to this category.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)

    recipes = relationship("Recipe", secondary="recipe_categories", back_populates="categories")
