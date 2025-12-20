from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from docuisine.db.models import User
from docuisine.utils.errors import UserExistsError, UserNotFoundError
from docuisine.utils.hashing import hash_in_sha256


class UserService:
    def __init__(self, db_session: Session):
        self.db_session: Session = db_session

    def create_user(self, username: str, password: str, email: Optional[str] = None) -> User:
        """
        Create a new user in the database with an encrypted password.

        Parameters
        ----------
        username : str
            The username of the new user. Must be unique.
        password : str
            The plain-text password to be encrypted and stored.

        Returns
        -------
        User
            The newly created `User` instance.

        Raises
        ------
        UserExistsError
            If a user with the same email already exists in the database.

        Notes
        -----
        - The password is encrypted using SHA-256 before storage.
        - This method commits the transaction immediately.
        """
        encrypted_password = hash_in_sha256(password)
        new_user = User(username=username, password=encrypted_password, email=email)
        try:
            self.db_session.add(new_user)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise UserExistsError(username)
        return new_user

    def get_user(self, user_id: Optional[int] = None, username: Optional[str] = None) -> User:
        """
        Retrieve a user from the database by ID or username.

        Parameters
        ----------
        user_id : int, optional
            The unique ID of the user to retrieve. Default is None.
        username : str, optional
            The username of the user to retrieve. Default is None.

        Returns
        -------
        User
            The `User` instance matching the provided ID or username.

        Raises
        ------
        ValueError
            If neither `user_id` nor `username` is provided.
        UserNotFoundError
            If no user is found with the given criteria.

        Notes
        -----
        - If both `user_id` and `username` are provided, `user_id` takes precedence.
        """
        if user_id is not None:
            result = self._get_user_by_id(user_id=user_id)
        elif username is not None:
            result = self._get_user_by_username(username=username)
        else:
            raise ValueError("Either user ID or username must be provided.")

        if result is None:
            raise (
                UserNotFoundError(user_id=user_id)
                if user_id is not None
                else UserNotFoundError(username=username)
            )

        return result

    def get_all_users(self) -> list[User]:
        """
        Retrieve all users from the database.

        Returns
        -------
        list[User]
            A list of all `User` instances in the database.
        """
        return self.db_session.query(User).all()

    def delete_user(self, user_id: int) -> None:
        """
        Delete a user from the database by their unique ID.

        Parameters
        ----------
        user_id : int
            The unique ID of the user to delete.

        Raises
        ------
        UserNotFoundError
            If no user is found with the given ID.

        Notes
        -----
        - This method commits the transaction immediately.
        """
        user = self._get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)
        self.db_session.delete(user)
        self.db_session.commit()

    def _get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user from the database by their unique ID.

        Parameters
        ----------
        user_id : int
            The unique ID of the user to retrieve.

        Returns
        -------
        Optional[User]
            The `User` instance if found, otherwise `None`.

        Notes
        -----
        No business logic should be placed here.
        """
        return self.db_session.query(User).filter_by(id=user_id).first()

    def _get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user from the database by their username.
        No business logic should be placed here.

        Parameters
        ----------
        username : str
            The username of the user to retrieve.

        Returns
        -------
        Optional[User]
            The `User` instance if found, otherwise `None`.

        Notes
        -----
        No business logic should be placed here.
        """
        return self.db_session.query(User).filter_by(username=username).first()

    def update_user_email(self, user_id: int, new_email: str) -> User:
        """
        Update the email address of an existing user.

        Parameters
        ----------
        user_id : int
            The unique ID of the user whose email is to be updated.
        new_email : str
            The new email address to set for the user.

        Returns
        -------
        User
            The updated `User` instance.

        Raises
        ------
        UserNotFoundError
            If no user is found with the given ID.

        Notes
        -----
        - This method commits the transaction immediately.
        """
        user = self._get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)
        user.email = new_email
        self.db_session.commit()
        return user


    def update_user_password(self, user_id: int, new_password: str) -> User:
        """
        Update the password of an existing user.

        Parameters
        ----------
        user_id : int
            The unique ID of the user whose password is to be updated.
        new_password : str
            The new plain-text password to be encrypted and set for the user.

        Returns
        -------
        User
            The updated `User` instance.

        Raises
        ------
        UserNotFoundError
            If no user is found with the given ID.

        Notes
        -----
        - The new password is encrypted using SHA-256 before storage.
        - This method commits the transaction immediately.
        """
        user = self._get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)
        encrypted_password = hash_in_sha256(new_password)
        user.password = encrypted_password
        self.db_session.commit()
        return user
