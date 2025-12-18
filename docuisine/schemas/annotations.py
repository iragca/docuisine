from typing import Annotated

from annotated_types import Len, MinLen
from fastapi import Depends
from pydantic import AfterValidator
from sqlalchemy.orm import Session

from docuisine.db.database import SessionLocal
from docuisine.utils.validation import validate_password, validate_version

CommitHash = Annotated[str, Len(7, 7)]
Password = Annotated[
    str, Len(min_length=8, max_length=128), AfterValidator(validate_password)
]  # Unhashed password
Version = Annotated[str, MinLen(5), AfterValidator(validate_version)]


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_session = Annotated[Session, Depends(get_db_session)]
