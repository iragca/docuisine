from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class IngredientCreate(BaseModel):
    name: str = Field(..., description="The ingredient name", examples=["Sugar", "Flour"])
    description: Optional[str] = Field(
        None, description="The ingredient description", examples=["Granulated white sugar"]
    )
    recipe_id: Optional[int] = Field(
        None, description="Recipe ID that produces this ingredient", examples=[1]
    )


class IngredientUpdate(BaseModel):
    name: Optional[str] = Field(None, description="The ingredient name", examples=["Sugar"])
    description: Optional[str] = Field(
        None, description="The ingredient description", examples=["Granulated white sugar"]
    )
    recipe_id: Optional[int] = Field(
        None, description="Recipe ID that produces this ingredient", examples=[1]
    )


class IngredientOut(BaseModel):
    id: int = Field(..., description="The ingredient's unique identifier", examples=[1])
    name: str = Field(..., description="The ingredient name", examples=["Sugar"])
    description: Optional[str] = Field(
        None, description="The ingredient description", examples=["Granulated white sugar"]
    )
    recipe_id: Optional[int] = Field(
        None, description="Recipe ID that produces this ingredient", examples=[1]
    )

    model_config = ConfigDict(from_attributes=True)
