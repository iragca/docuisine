from enum import Enum


class ErrorCode(str, Enum):
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"


class Status(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
