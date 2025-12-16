from enum import Enum
from typing import Annotated

from annotated_types import Len, MinLen
from pydantic import AfterValidator


def _has_two_dots(version: str) -> str:
    if version.count(".") == 2:
        return version

    raise ValueError("Version must have two dots (e.g., '1.0.0').")


def _has_only_digits(version: str) -> str:
    if all(part.isdigit() for part in version.split(".")):
        return version
    raise ValueError("Version parts must be numeric.")


CommitHash = Annotated[str, Len(7, 7)]
Version = Annotated[
    str, MinLen(5), AfterValidator(_has_two_dots), AfterValidator(_has_only_digits)
]


class Status(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
