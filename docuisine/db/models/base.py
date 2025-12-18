from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Entity:
    """
    Base entity model with common attributes.

    Attributes:
        id (int): Primary key identifier for the entity.
        preview_img (Optional[str]): URL or path to the preview image.
        img (Optional[str]): URL or path to the main image.
        created_at (datetime): Timestamp when the entity was created.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    preview_img: Mapped[Optional[str]]
    img: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now(timezone.utc))
