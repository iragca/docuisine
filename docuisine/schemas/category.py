from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Entity


class CategoryCreate(Entity):
    name: str = Field(..., description="The category name", examples=["Dessert", "Vegetarian"])
    description: Optional[str] = Field(
        None, description="The category description", examples=["Sweet dishes and treats"]
    )


class CategoryUpdate(Entity):
    name: Optional[str] = Field(None, description="The category name", examples=["Dessert"])
    description: Optional[str] = Field(
        None, description="The category description", examples=["Sweet dishes and treats"]
    )


class CategoryRead(BaseModel):
    id: int = Field(..., description="The category's unique identifier", examples=[1])


class CategoryOut(Entity):
    id: int = Field(..., description="The category's unique identifier", examples=[1])
    name: str = Field(..., description="The category name", examples=["Dessert"])
    description: Optional[str] = Field(
        None, description="The category description", examples=["Sweet dishes and treats"]
    )

    model_config = ConfigDict(from_attributes=True)
