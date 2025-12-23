from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RecipeCreate(BaseModel):
    name: str = Field(..., description="Recipe name", examples=["Chocolate Cake"])
    cook_time_sec: Optional[int] = Field(
        None, description="Cooking time in seconds", examples=[3600]
    )
    prep_time_sec: Optional[int] = Field(
        None, description="Preparation time in seconds", examples=[1200]
    )
    non_blocking_time_sec: Optional[int] = Field(
        None, description="Non-blocking time in seconds", examples=[600]
    )
    servings: Optional[int] = Field(None, description="Number of servings", examples=[8])
    description: Optional[str] = Field(
        None, description="Recipe description", examples=["Delicious chocolate cake"]
    )


class RecipeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Recipe name")
    cook_time_sec: Optional[int] = Field(None, description="Cooking time in seconds")
    prep_time_sec: Optional[int] = Field(None, description="Preparation time in seconds")
    non_blocking_time_sec: Optional[int] = Field(None, description="Non-blocking time in seconds")
    servings: Optional[int] = Field(None, description="Number of servings")
    description: Optional[str] = Field(None, description="Recipe description")


class RecipeOut(BaseModel):
    id: int = Field(..., description="Recipe's unique identifier", examples=[1])
    user_id: int = Field(..., description="ID of the user who created the recipe", examples=[1])
    name: str = Field(..., description="Recipe name", examples=["Chocolate Cake"])
    cook_time_sec: Optional[int] = Field(None, description="Cooking time in seconds")
    prep_time_sec: Optional[int] = Field(None, description="Preparation time in seconds")
    non_blocking_time_sec: Optional[int] = Field(None, description="Non-blocking time in seconds")
    servings: Optional[int] = Field(None, description="Number of servings")
    description: Optional[str] = Field(None, description="Recipe description")

    model_config = ConfigDict(from_attributes=True)
