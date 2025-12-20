from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from docuisine.schemas import Role

from .base import Base, Entity


class User(Base, Entity):
    """
    User model representing a user in the system.

    Attributes
    ----------
    id : int
        Primary key identifier for the user.
    username : str
        Unique username of the user.
    email : Optional[str]
        Unique email address of the user. May be ``None``.
    password : str
        Hashed password of the user.
    role : str
        Role of the user in the system (e.g., ``admin``, ``user``).
    recipes : list[Recipe]
        Recipes created by the user.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(nullable=False, default=Role.USER.value)

    recipes = relationship("Recipe", back_populates="creator")
