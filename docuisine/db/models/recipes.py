from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, Entity


class Recipe(Base, Entity):
    """
    Recipe model representing a cooking recipe.

    Attributes
    ----------
    id : int
        Primary key identifier for the recipe.
    user_id : int
        Foreign key to the user who created the recipe.
    name : str
        Name of the recipe.
    cook_time_sec : int
        Cooking time in seconds.
    prep_time_sec : int
        Preparation time in seconds.
    non_blocking_time_sec : int
        Non-blocking time in seconds.
    servings : int
        Number of servings the recipe yields.
        One serving is fit for one person.
    description : str
        Description of the recipe.
    """

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    cook_time_sec: Mapped[int] = mapped_column(nullable=True)
    prep_time_sec: Mapped[int] = mapped_column(nullable=True)
    non_blocking_time_sec: Mapped[int] = mapped_column(nullable=True)
    servings: Mapped[int] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    creator = relationship("User", back_populates="recipes")
    steps = relationship("RecipeStep", back_populates="recipe", cascade="all, delete-orphan")
    ingredients = relationship(
        "Ingredient", secondary="recipe_ingredients", back_populates="recipes"
    )
    categories = relationship("Category", secondary="recipe_categories", back_populates="recipes")
    product = relationship(
        "Ingredient",
        back_populates="recipe",
    )

    __table_args__ = (
        CheckConstraint("cook_time_sec >= 0", name="cook_time_non_negative"),
        CheckConstraint("prep_time_sec >= 0", name="prep_time_non_negative"),
        CheckConstraint("non_blocking_time_sec >= 0", name="non_blocking_time_non_negative"),
        CheckConstraint("servings >= 0", name="servings_non_negative"),
    )


class RecipeStep(Base, Entity):
    """
    RecipeStep model representing a step in a recipe.

    Attributes
    ----------
    recipe_id : int
        Foreign key to the associated recipe.
    step_number : int
        The order number of the step in the recipe.
    description : str
        Description of the step.
    """

    __tablename__ = "recipe_steps"

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    step_number: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)

    recipe = relationship("Recipe", back_populates="steps")

    __table_args__ = (CheckConstraint("step_number >= 1", name="step_number_positive"),)


class RecipeIngredient(Base, Entity):
    """
    RecipeIngredient model representing an ingredient in a recipe.

    Attributes
    ----------
    recipe_id : int
        Foreign key to the associated recipe.
    ingredient_id : int
        Foreign key to the associated ingredient.
    amount_grams : float
        Amount of the ingredient in grams.
    amount_readable : str
        Human-readable amount of the ingredient.
    """

    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    amount_grams: Mapped[int] = mapped_column(nullable=False)
    amount_readable: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (CheckConstraint("amount_grams >= 0", name="amount_grams_non_negative"),)


class RecipeCategory(Base, Entity):
    """
    Association table for many-to-many relationship between Recipe and Category.

    Attributes:
        recipe_id (int): Foreign key to the associated recipe.
        category_id (int): Foreign key to the associated category.
    """

    __tablename__ = "recipe_categories"
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)
