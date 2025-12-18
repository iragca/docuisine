from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from docuisine.core.config import env
from docuisine.db.models.base import Base
from docuisine.schemas.enums import Mode


def IS_PRODUCTION() -> bool:
    """
    Check if the application is running in production mode.

    Raises
    ------
        ValueError
            If the MODE environment variable is not set to a valid value.
    """
    mode = env.MODE
    if mode not in (Mode.DEVELOPMENT, Mode.PRODUCTION, Mode.TESTING):
        raise ValueError(
            f"Invalid MODE: {mode}. Must be one of: development, production, testing."
        )
    return env.MODE == Mode.PRODUCTION


_engine = create_engine(env.DATABASE_URL, echo=not IS_PRODUCTION())
Base.metadata.create_all(bind=_engine)
SessionLocal = sessionmaker(bind=_engine)
