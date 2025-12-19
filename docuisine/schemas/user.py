from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from docuisine.schemas.annotations import Password, Username


class UserCreate(BaseModel):
    username: Username = Field(..., description="The user's username", examples=["user123"])
    password: Password = Field(
        description="The user's password",
        examples=["strongPassword123!", "01fKl%#RJa4~Ob)'BER]"],
    )


class UserRead(BaseModel):
    id: int = Field(..., description="The user's unique identifier", examples=[1])


class UserOut(BaseModel):
    id: int = Field(..., description="The user's unique identifier", examples=[1])
    username: Optional[Username] = Field(
        None, description="The user's username", examples=["user123"]
    )
    email: Optional[EmailStr] = Field(
        None, description="The user's email address", examples=["user@example.com"]
    )

    model_config = ConfigDict(from_attributes=True)
