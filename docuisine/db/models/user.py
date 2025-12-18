from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from docuisine.schemas import Role

from .base import Base


class User(Base):
    """
    User model representing a user in the system.

    Attributes:
        id (int): Primary key identifier for the user.
        email (str): Unique email address of the user.
        password (str): Hashed password of the user.
        role (str): Role of the user in the system (e.g., admin, user).
        created_at (datetime): Timestamp when the user was created.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(String, nullable=False, default=Role.USER.value)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

