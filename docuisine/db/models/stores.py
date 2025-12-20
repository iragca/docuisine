from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, Entity


class Store(Base, Entity):
    """
    Store model representing a store location.

    Attributes
    ----------
    id : int
        Primary key identifier for the store.
    name : str
        Name of the store.
    longitude : float
        Longitude of the store location.
    latitude : float
        Latitude of the store location.
    address : str
        Address of the store.
    phone : str
        Phone number of the store.
    website : str
        Website URL of the store.
    description : str
        Description of the store.
    ingredients : List[Ingredient]
        Ingredients stocked by the store.
    """

    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    longitude: Mapped[Optional[float]] = mapped_column(nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(nullable=True)
    website: Mapped[Optional[str]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)

    ingredients = relationship("Ingredient", secondary="shelves", back_populates="stores")

    __table_args__ = (
        CheckConstraint("longitude >= -180 AND longitude <= 180", name="longitude_range_check"),
        CheckConstraint("latitude >= -90 AND latitude <= 90", name="latitude_range_check"),
    )


class Shelf(Base, Entity):
    """
    Shelf model representing a shelf storing ingredients in a store.

    Attributes
    ----------
    store_id : int
        Foreign key to the associated store.
    ingredient_id : int
        Foreign key to the associated ingredient.
    quantity : int
        Quantity of the ingredient on the shelf.
    """

    __tablename__ = "shelves"

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (CheckConstraint("quantity >= 0", name="shelf_quantity_non_negative"),)
