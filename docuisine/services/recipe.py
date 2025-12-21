from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from docuisine.db.models import Recipe
from docuisine.utils.errors.recipe import RecipeExistsError, RecipeNotFoundError


class RecipeService:
    def __init__(self, db_session: Session):
        self.db_session: Session = db_session

    def create_recipe(
        self,
        user_id: int,
        name: str,
        cook_time_sec: Optional[int] = None,
        prep_time_sec: Optional[int] = None,
        non_blocking_time_sec: Optional[int] = None,
        servings: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Recipe:
        """
        Create a new recipe in the database.

        Parameters
        ----------
        user_id : int
            The ID of the user creating the recipe.
        name : str
            The name of the recipe.
        cook_time_sec : Optional[int]
            Cooking time in seconds. Default is None.
        prep_time_sec : Optional[int]
            Preparation time in seconds. Default is None.
        non_blocking_time_sec : Optional[int]
            Non-blocking time in seconds. Default is None.
        servings : Optional[int]
            Number of servings. Default is None.
        description : Optional[str]
            Description of the recipe. Default is None.

        Returns
        -------
        Recipe
            The newly created `Recipe` instance.

        Raises
        ------
        RecipeExistsError
            If a recipe with the same name already exists.
        """
        new_recipe = Recipe(
            user_id=user_id,
            name=name,
            cook_time_sec=cook_time_sec,
            prep_time_sec=prep_time_sec,
            non_blocking_time_sec=non_blocking_time_sec,
            servings=servings,
            description=description,
        )
        try:
            self.db_session.add(new_recipe)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise RecipeExistsError(name)
        return new_recipe

    def get_recipe(self, recipe_id: Optional[int] = None, name: Optional[str] = None) -> Recipe:
        """
        Retrieve a recipe by ID or name.

        Parameters
        ----------
        recipe_id : Optional[int]
            The unique ID of the recipe.
        name : Optional[str]
            The name of the recipe.

        Returns
        -------
        Recipe
            The `Recipe` instance matching the criteria.

        Raises
        ------
        ValueError
            If neither recipe_id nor name is provided.
        RecipeNotFoundError
            If no recipe is found.

        Notes
        -----
        - If both are provided, `recipe_id` takes precedence.
        """
        if recipe_id is not None:
            result = self._get_recipe_by_id(recipe_id=recipe_id)
        elif name is not None:
            result = self._get_recipe_by_name(name=name)
        else:
            raise ValueError("Either recipe ID or name must be provided.")

        if result is None:
            raise (
                RecipeNotFoundError(recipe_id=recipe_id)
                if recipe_id is not None
                else RecipeNotFoundError(name=name)
            )

        return result

    def get_all_recipes(self) -> list[Recipe]:
        """Retrieve all recipes from the database."""
        return self.db_session.query(Recipe).all()

    def get_recipes_by_user(self, user_id: int) -> list[Recipe]:
        """
        Retrieve all recipes created by a specific user.

        Parameters
        ----------
        user_id : int
            The ID of the user.

        Returns
        -------
        list[Recipe]
            A list of `Recipe` instances created by the user.
        """
        return self.db_session.query(Recipe).filter_by(user_id=user_id).all()

    def update_recipe(
        self,
        recipe_id: int,
        name: Optional[str] = None,
        cook_time_sec: Optional[int] = None,
        prep_time_sec: Optional[int] = None,
        non_blocking_time_sec: Optional[int] = None,
        servings: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Recipe:
        """
        Update an existing recipe's fields.

        Parameters
        ----------
        recipe_id : int
            The unique ID of the recipe to update.
        name : Optional[str]
            New name. Default is None (no change).
        cook_time_sec : Optional[int]
            New cooking time. Default is None (no change).
        prep_time_sec : Optional[int]
            New preparation time. Default is None (no change).
        non_blocking_time_sec : Optional[int]
            New non-blocking time. Default is None (no change).
        servings : Optional[int]
            New servings count. Default is None (no change).
        description : Optional[str]
            New description. Default is None (no change).

        Returns
        -------
        Recipe
            The updated `Recipe` instance.

        Raises
        ------
        RecipeNotFoundError
            If no recipe exists with `recipe_id`.
        RecipeExistsError
            If updating the name conflicts with an existing recipe.
        """
        recipe = self._get_recipe_by_id(recipe_id)
        if recipe is None:
            raise RecipeNotFoundError(recipe_id=recipe_id)

        if name is not None:
            recipe.name = name
        if cook_time_sec is not None:
            recipe.cook_time_sec = cook_time_sec
        if prep_time_sec is not None:
            recipe.prep_time_sec = prep_time_sec
        if non_blocking_time_sec is not None:
            recipe.non_blocking_time_sec = non_blocking_time_sec
        if servings is not None:
            recipe.servings = servings
        if description is not None:
            recipe.description = description

        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise RecipeExistsError(name if name is not None else recipe.name)

        return recipe

    def delete_recipe(self, recipe_id: int) -> None:
        """
        Delete a recipe from the database by its unique ID.

        Parameters
        ----------
        recipe_id : int
            The unique ID of the recipe to delete.

        Raises
        ------
        RecipeNotFoundError
            If no recipe is found with the given ID.
        """
        recipe = self._get_recipe_by_id(recipe_id)
        if recipe is None:
            raise RecipeNotFoundError(recipe_id=recipe_id)
        self.db_session.delete(recipe)
        self.db_session.commit()

    def _get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """
        Retrieve a recipe from the database by its unique ID.

        Parameters
        ----------
        recipe_id : int
            The unique ID of the recipe to retrieve.

        Returns
        -------
        Optional[Recipe]
            The `Recipe` instance if found, otherwise `None`.

        Notes
        -----
        No business logic should be placed here.
        """
        return self.db_session.query(Recipe).filter_by(id=recipe_id).first()

    def _get_recipe_by_name(self, name: str) -> Optional[Recipe]:
        """
        Retrieve a recipe from the database by its name.

        Parameters
        ----------
        name : str
            The name of the recipe to retrieve.

        Returns
        -------
        Optional[Recipe]
            The `Recipe` instance if found, otherwise `None`.

        Notes
        -----
        No business logic should be placed here.
        """
        return self.db_session.query(Recipe).filter_by(name=name).first()
