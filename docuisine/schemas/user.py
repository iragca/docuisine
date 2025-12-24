from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from docuisine.schemas.annotations import Password, Username
from docuisine.schemas.common import Default, Entity


class UserCreate(BaseModel):
    username: Username = Field(..., description="The user's username", examples=["user123"])
    email: Optional[EmailStr] = Field(
        None, description="The user's email address", examples=["user@example.com"]
    )
    password: Password = Field(
        description="The user's password",
        examples=["strongPassword123!", "01fKl%#RJa4~Ob)'BER]"],
    )


class UserUpdateEmail(BaseModel):
    id: int = Field(..., description="The user's unique identifier", examples=[1])
    password: Password = Field(
        ..., description="The user's password", examples=["CurrentPassword!23"]
    )
    email: EmailStr = Field(
        ..., description="The user's email address", examples=["example@mail.com"]
    )


class UserUpdatePassword(BaseModel):
    id: int = Field(..., description="The user's unique identifier", examples=[1])
    old_password: Password = Field(
        ..., description="The user's current password", examples=["CurrentPassword!23"]
    )
    new_password: Password = Field(
        ..., description="The user's new password", examples=["NewStrongPassword!45"]
    )


class UserRead(BaseModel):
    id: int = Field(..., description="The user's unique identifier", examples=[1])


class UserUpdate(Entity):
    id: int = Field(..., description="The user's unique identifier", examples=[1])
    username: Optional[Username] = Field(
        None, description="The user's username", examples=["user123"]
    )
    email: Optional[EmailStr] = Field(
        None, description="The user's email address", examples=["user@example.com"]
    )


class UserOut(Entity, Default):
    id: int = Field(..., description="The user's unique identifier", examples=[1])
    username: Optional[Username] = Field(
        None, description="The user's username", examples=["user123"]
    )
    email: Optional[EmailStr] = Field(
        None, description="The user's email address", examples=["user@example.com"]
    )

    model_config = ConfigDict(from_attributes=True)
