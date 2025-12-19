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
        - Returns `None` if no user is found with the given criteria.
        """
        if user_id is None and username is None:
            raise ValueError("Either user ID or username must be provided.")
        if user_id is not None:
            result = self.db_session.query(User).filter_by(id=user_id).first()
        else:
            result = self.db_session.query(User).filter_by(username=username).first()

        if result is None:
            raise (
                UserNotFoundError(user_id=user_id)
                if user_id is not None
                else UserNotFoundError(username=username)
            )

        return result

    def get_all_users(self) -> list[User]:
        return self.db_session.query(User).all()
