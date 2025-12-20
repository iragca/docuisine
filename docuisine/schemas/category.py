from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., description="The category name", examples=["Dessert", "Vegetarian"])
    description: Optional[str] = Field(
        None, description="The category description", examples=["Sweet dishes and treats"]
    )


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, description="The category name", examples=["Dessert"])
    description: Optional[str] = Field(
        None, description="The category description", examples=["Sweet dishes and treats"]
    )


class CategoryRead(BaseModel):
    id: int = Field(..., description="The category's unique identifier", examples=[1])


class CategoryOut(BaseModel):
    id: int = Field(..., description="The category's unique identifier", examples=[1])
    name: str = Field(..., description="The category name", examples=["Dessert"])
    description: Optional[str] = Field(
        None, description="The category description", examples=["Sweet dishes and treats"]
    )

    model_config = ConfigDict(from_attributes=True)
