from typing import Optional

from docuisine.db.models import User
from docuisine.schemas.user import UserCreate
from docuisine.utils.hashing import hash_in_sha256


class UserService:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_user(self, user: UserCreate) -> User:
        encrypted_password = hash_in_sha256(user.password)
        new_user = User(email=user.email, password=encrypted_password)
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def get_user(self, user_id: Optional[int] = None, email: Optional[str] = None) -> User:
        """
        Retrieve a user from the database by ID or email.

        Parameters
        ----------
        user_id : int, optional
            The unique ID of the user to retrieve. Default is None.
        email : str, optional
            The email of the user to retrieve. Default is None.

        Returns
        -------
        User
            The `User` instance matching the provided ID or email.

        Raises
        ------
        ValueError
            If neither `user_id` nor `email` is provided.

        Notes
        -----
        - If both `user_id` and `email` are provided, `user_id` takes precedence.
        - Returns `None` if no user is found with the given criteria.
        """
        if user_id is None and email is None:
            raise ValueError("Either user ID or email must be provided.")
        if user_id is not None:
            return self.db_session.query(User).filter_by(id=user_id).first()
        else:
            return self.db_session.query(User).filter_by(email=email).first()

    def get_all_users(self) -> list[User]:
        return self.db_session.query(User).all()
