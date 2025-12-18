import os
import subprocess
from typing import Union

from dotenv import load_dotenv
from sqlalchemy.util import classproperty


class Environment:
    """Lazy-loaded application info, cached for efficiency."""

    def __init__(self) -> None:
        load_dotenv()

    @classproperty
    def DATABASE_URL(self) -> str:
        URL = os.getenv("DATABASE_URL")
        if URL is None:
            raise EnvironmentError("DATABASE_URL environment variable is not set.")
        return URL

    @classproperty
    def COMMIT_HASH(self) -> Union[str, None]:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )

    @classproperty
    def VERSION(self) -> Union[str, None]:
        return (
            subprocess.check_output(["uv", "version", "--short"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )

    @classproperty
    def MODE(self) -> str:
        mode = os.getenv("MODE")
        if mode is None:
            raise EnvironmentError("MODE environment variable is not set.")
        return mode


env = Environment()
