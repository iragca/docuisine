from typing import Annotated

from annotated_types import Len, MinLen
from fastapi import File, Form, UploadFile
from pydantic import AfterValidator

from docuisine.utils.validation import validate_password, validate_version

CommitHash = Annotated[str, Len(7, 7)]
Username = Annotated[str, MinLen(3)]
Password = Annotated[
    str, Len(min_length=8, max_length=128), AfterValidator(validate_password)
]  # Unhashed password
Version = Annotated[str, MinLen(5), AfterValidator(validate_version)]
ImageUpload = Annotated[UploadFile, File()]


CategoryName = Annotated[
    str, Form(..., description="The category name", examples=["Dessert", "Vegetarian"])
]
CategoryDescription = Annotated[
    str,
    Form(..., description="The category description", examples=["Sweet dishes and treats"]),
]
