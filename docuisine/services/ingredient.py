from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from docuisine.db.models import Ingredient
from docuisine.utils.errors.ingredient import IngredientExistsError, IngredientNotFoundError


class IngredientService:
    def __init__(self, db_session: Session):
        self.db_session: Session = db_session

    def create_ingredient(
        self,
        name: str,
        description: Optional[str] = None,
        recipe_id: Optional[int] = None,
    ) -> Ingredient:
        """
        Create a new ingredient in the database.

        Parameters
        ----------
        name : str
            The name of the ingredient. Must be unique.
        description : Optional[str]
            A description of the ingredient. Default is None.
        recipe_id : Optional[int]
            A recipe ID that produces this ingredient (product), optional.

        Returns
        -------
        Ingredient
            The newly created `Ingredient` instance.

        Raises
        ------
        IngredientExistsError
            If an ingredient with the same name already exists.
        """
        new_ingredient = Ingredient(name=name, description=description, recipe_id=recipe_id)
        try:
            self.db_session.add(new_ingredient)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise IngredientExistsError(name)
        return new_ingredient

    def get_ingredient(
        self, ingredient_id: Optional[int] = None, name: Optional[str] = None
    ) -> Ingredient:
        """
        Retrieve an ingredient by ID or name.

        Parameters
        ----------
        ingredient_id : Optional[int]
            The unique ID of the ingredient to retrieve. Default is None.
        name : Optional[str]
            The name of the ingredient to retrieve. Default is None.

        Returns
        -------
        Ingredient
            The `Ingredient` instance matching the provided ID or name.

        Raises
        ------
        IngredientNotFoundError
            If no ingredient is found with the given ID or name.
        ValueError
            If neither `ingredient_id` nor `name` is provided.

        Notes
        -----
        - If both are provided, `ingredient_id` takes precedence.
        """
        if ingredient_id is not None:
            result = self._get_ingredient_by_id(ingredient_id=ingredient_id)
        elif name is not None:
            result = self._get_ingredient_by_name(name=name)
        else:
            raise ValueError("Either ingredient ID or name must be provided.")

        if result is None:
            raise (
                IngredientNotFoundError(ingredient_id=ingredient_id)
                if ingredient_id is not None
                else IngredientNotFoundError(name=name)
            )

        return result

    def get_all_ingredients(self) -> list[Ingredient]:
        """
        Return all ingredients.

        Returns
        -------
        list[Ingredient]
            A list of all `Ingredient` instances in the database.
        """
        return self.db_session.query(Ingredient).all()

    def update_ingredient(
        self,
        ingredient_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        recipe_id: Optional[int] = None,
    ) -> Ingredient:
        """
        Update an existing ingredient's fields.

        Parameters
        ----------
        ingredient_id : int
            The unique ID of the ingredient to update.
        name : Optional[str]
            The new name for the ingredient. Default is None.
        description : Optional[str]
            The new description for the ingredient. Default is None.
        recipe_id : Optional[int]
            The new recipe ID for the ingredient. Default is None.

        Returns
        -------
        Ingredient
            The updated `Ingredient` instance.

        Raises
        ------
        IngredientNotFoundError
            If no ingredient is found with the given ID.
        IngredientExistsError
            If an ingredient with the new name already exists.
        """
        ingredient = self._get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            raise IngredientNotFoundError(ingredient_id=ingredient_id)

        if name is not None:
            ingredient.name = name
        if description is not None:
            ingredient.description = description
        if recipe_id is not None:
            ingredient.recipe_id = recipe_id

        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            # Use provided name, otherwise current name
            raise IngredientExistsError(name if name is not None else ingredient.name)

        return ingredient

    def delete_ingredient(self, ingredient_id: int) -> None:
        """
        Delete an ingredient by ID.

        Raises
        ------
        IngredientNotFoundError
            If no ingredient is found with the given ID.
        """
        ingredient = self._get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            raise IngredientNotFoundError(ingredient_id=ingredient_id)
        self.db_session.delete(ingredient)
        self.db_session.commit()

    def _get_ingredient_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        """
        Primitive query: find ingredient by ID (no business logic).

        Returns
        -------
        Optional[Ingredient]
            The `Ingredient` instance if found, else None.
        """
        return self.db_session.query(Ingredient).filter_by(id=ingredient_id).first()

    def _get_ingredient_by_name(self, name: str) -> Optional[Ingredient]:
        """
        Primitive query: find ingredient by name (no business logic).

        Returns
        -------
        Optional[Ingredient]
            The `Ingredient` instance if found, else None.
        """
        return self.db_session.query(Ingredient).filter_by(name=name).first()
