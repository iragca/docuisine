from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from docuisine.db.models import Category
from docuisine.utils.errors.category import CategoryExistsError, CategoryNotFoundError


class CategoryService:
    def __init__(self, db_session: Session):
        self.db_session: Session = db_session

    def create_category(
        self,
        name: str,
        description: Optional[str] = None,
        img: Optional[str] = None,
        preview_img: Optional[str] = None,
    ) -> Category:
        """
        Create a new category in the database.

        Parameters
        ----------
        name : str
            The name of the new category. Must be unique.
        description : Optional[str]
            The description of the category. Default is None.
        img : Optional[str]
            The image URL for the category. Default is None.
        preview_img : Optional[str]
            The preview image URL for the category. Default is None.

        Returns
        -------
        Category
            The newly created `Category` instance.

        Raises
        ------
        CategoryExistsError
            If a category with the same name already exists in the database.

        Notes
        -----
        - This method commits the transaction immediately.
        """
        new_category = Category(
            name=name, description=description, img=img, preview_img=preview_img
        )
        try:
            self.db_session.add(new_category)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise CategoryExistsError(name)
        return new_category

    def get_category(
        self, category_id: Optional[int] = None, name: Optional[str] = None
    ) -> Category:
        """
        Retrieve a category from the database by ID or name.

        Parameters
        ----------
        category_id : int, optional
            The unique ID of the category to retrieve. Default is None.
        name : str, optional
            The name of the category to retrieve. Default is None.

        Returns
        -------
        Category
            The `Category` instance matching the provided ID or name.

        Raises
        ------
        ValueError
            If neither `category_id` nor `name` is provided.
        CategoryNotFoundError
            If no category is found with the given criteria.

        Notes
        -----
        - If both `category_id` and `name` are provided, `category_id` takes precedence.
        """
        if category_id is not None:
            result = self._get_category_by_id(category_id=category_id)
        elif name is not None:
            result = self._get_category_by_name(name=name)
        else:
            raise ValueError("Either category ID or name must be provided.")

        if result is None:
            raise (
                CategoryNotFoundError(category_id=category_id)
                if category_id is not None
                else CategoryNotFoundError(name=name)
            )

        return result

    def get_all_categories(self) -> list[Category]:
        """
        Retrieve all categories from the database.

        Returns
        -------
        list[Category]
            A list of all `Category` instances in the database.
        """
        return self.db_session.query(Category).all()

    def update_category(
        self,
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Category:
        """
        Update an existing category's name and/or description.

        Parameters
        ----------
        category_id : int
            The unique ID of the category to update.
        name : Optional[str]
            The new name for the category. Default is None (no change).
        description : Optional[str]
            The new description for the category. Default is None (no change).

        Returns
        -------
        Category
            The updated `Category` instance.

        Raises
        ------
        CategoryNotFoundError
            If no category is found with the given ID.
        CategoryExistsError
            If updating the name would conflict with an existing category.

        Notes
        -----
        - This method commits the transaction immediately.
        - At least one of `name` or `description` should be provided.
        """
        category = self._get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(category_id=category_id)

        if name is not None:
            category.name = name
        if description is not None:
            category.description = description

        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise CategoryExistsError(name if name is not None else category.name)

        return category

    def delete_category(self, category_id: int) -> None:
        """
        Delete a category from the database by its unique ID.

        Parameters
        ----------
        category_id : int
            The unique ID of the category to delete.

        Raises
        ------
        CategoryNotFoundError
            If no category is found with the given ID.

        Notes
        -----
        - This method commits the transaction immediately.
        """
        category = self._get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(category_id=category_id)
        self.db_session.delete(category)
        self.db_session.commit()

    def _get_category_by_id(self, category_id: int) -> Optional[Category]:
        """
        Retrieve a category from the database by its unique ID.

        Parameters
        ----------
        category_id : int
            The unique ID of the category to retrieve.

        Returns
        -------
        Optional[Category]
            The `Category` instance if found, otherwise `None`.

        Notes
        -----
        No business logic should be placed here.
        """
        return self.db_session.query(Category).filter_by(id=category_id).first()

    def _get_category_by_name(self, name: str) -> Optional[Category]:
        """
        Retrieve a category from the database by its name.

        Parameters
        ----------
        name : str
            The name of the category to retrieve.

        Returns
        -------
        Optional[Category]
            The `Category` instance if found, otherwise `None`.

        Notes
        -----
        No business logic should be placed here.
        """
        return self.db_session.query(Category).filter_by(name=name).first()
