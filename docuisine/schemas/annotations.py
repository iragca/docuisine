from typing import Annotated

from annotated_types import Len, MinLen
from pydantic import AfterValidator

from docuisine.utils.validation import validate_password, validate_version

CommitHash = Annotated[str, Len(7, 7)]
Password = Annotated[str, Len(min_length=8, max_length=128), AfterValidator(validate_password)]
Version = Annotated[str, MinLen(5), AfterValidator(validate_version)]
