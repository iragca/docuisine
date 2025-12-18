from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from docuisine.schemas.annotations import Password


class UserCreate(BaseModel):
    email: EmailStr = Field(
        ..., description="The user's email address", examples=["user@example.com"]
    )
    password: Password = Field(
        min_length=16,
        description="The user's password",
        examples=["strongPassword123!", "01fKl%#RJa4~Ob)'BER]"],
    )


class UserRead(BaseModel):
    id: int = Field(..., description="The user's unique identifier", examples=[1])


class UserOut(BaseModel):
    id: int = Field(..., description="The user's unique identifier", examples=[1])
    email: Optional[EmailStr] = Field(
        None, description="The user's email address", examples=["user@example.com"]
    )

    model_config = ConfigDict(from_attributes=True)
