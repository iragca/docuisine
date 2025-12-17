from docuisine.db.models import User
from docuisine.schemas.user import UserCreate, UserRead
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

    def get_user(self, user: UserRead) -> User:
        if user.id is None and user.email is None:
            raise ValueError("Either user ID or email must be provided.")
        if user.id is not None:
            return self.db_session.query(User).filter_by(id=user.id).first()
        else:
            return self.db_session.query(User).filter_by(email=user.email).first()

    def get_all_users(self) -> list[User]:
        return self.db_session.query(User).all()
