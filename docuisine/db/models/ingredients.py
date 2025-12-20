from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, Entity


class Ingredient(Base, Entity):
    """
    Ingredient model representing an ingredient in a recipe.

    Attributes
    ----------
    id : int
        Primary key identifier for the ingredient.
    name : str
        Name of the ingredient.
    description : Optional[str]
        Description of the ingredient.
    recipe_id : Optional[int]
        The recipe to make this ingredient from, if applicable. May be ``None``.
    recipe : Optional[Recipe]
        The recipe to make this ingredient from, if applicable. May be ``None``.
    recipes : List[Recipe]
        Recipes that use this ingredient.
    stores : List[Store]
        Stores that stock this ingredient.
    """

    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    recipe_id: Mapped[Optional[int]] = mapped_column(ForeignKey("recipes.id"), nullable=True)

    recipe = relationship("Recipe", back_populates="product")
    recipes = relationship("Recipe", secondary="recipe_ingredients", back_populates="ingredients")
    stores = relationship("Store", secondary="shelves", back_populates="ingredients")
