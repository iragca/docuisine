from typing import Annotated

from annotated_types import Len, MinLen
from pydantic import AfterValidator

from docuisine.utils.validation import validate_version

CommitHash = Annotated[str, Len(7, 7)]
Version = Annotated[str, MinLen(5), AfterValidator(validate_version)]
