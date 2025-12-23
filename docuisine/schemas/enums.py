from enum import Enum


class Status(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    PUBLIC = "public"


class Mode(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class TokenType(str, Enum):
    """
    Types of tokens used for authentication in the request header.
    """

    BEARER = "bearer"
    REFRESH = "refresh"


class JWTAlgorithm(str, Enum):
    """
    Supported JWT signing algorithms.
    """

    HS256 = "HS256"
