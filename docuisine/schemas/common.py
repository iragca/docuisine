from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Detail(BaseModel):
    """
    Schema for detail messages in HTTP responses.
    Often used to convey error messages or other informational text
    in the API or routes.
    """

    detail: str


class Default(BaseModel):
    """
    Default schema with common attributes.

    Attributes
    ----------
    created_at : datetime
        Timestamp when the record was created.
    updated_at : datetime
        Timestamp when the record was last updated.
    """

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Entity(BaseModel):
    """
    Base schema for entities with an ID.

    Attributes
    ----------
    img : Optional[str]
        URL or path to the main image.
    preview_img : Optional[str]
        URL or path to the preview image.
    """

    img: Optional[str] = Field(
        None, description="URL or path to the main image", examples=["image.jpg"]
    )
    preview_img: Optional[str] = Field(
        None, description="URL or path to the preview image", examples=["preview_image.jpg"]
    )
