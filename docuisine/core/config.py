import os
from typing import Optional

from dotenv import load_dotenv


class Environment:
    """Environment configuration loader."""

    def __init__(self) -> None:
        load_dotenv()

    @property
    def DATABASE_URL(self) -> str:
        URL = os.getenv("DATABASE_URL")
        if URL is None:
            raise EnvironmentError("DATABASE_URL environment variable is not set.")
        return URL

    @property
    def COMMIT_HASH(self) -> Optional[str]:
        return os.getenv("COMMIT_HASH", None)

    @property
    def VERSION(self) -> Optional[str]:
        return os.getenv("VERSION", None)

    @property
    def MODE(self) -> str:
        mode = os.getenv("MODE")
        if mode is None:
            raise EnvironmentError("MODE environment variable is not set.")
        return mode

    @property
    def JWT_SECRET_KEY(self) -> str:
        secret_key = os.getenv("JWT_SECRET_KEY", None)
        if secret_key is None:
            raise EnvironmentError("JWT_SECRET_KEY environment variable is not set.")
        return secret_key

    @property
    def JWT_ALGORITHM(self) -> str:
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        return algorithm

    @property
    def JWT_ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        expire_minutes = os.getenv(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "525600"
        )  # Default to 1 year
        return int(expire_minutes)


env = Environment()
