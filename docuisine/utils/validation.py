import re
from typing import Iterable, Literal, Optional

from docuisine.schemas.enums import Role
from docuisine.utils import errors


def has_two_dots(version: str) -> str:
    """
    Validate that the version string has exactly two dots.

    Parameters
    ----------
    version : str
        The version string to validate.

    Returns
    -------
    str
        The version string if it is valid.

    Raises
    ------
    ValueError
        If the version string does not have exactly two dots.
    """
    if version.count(".") == 2:
        return version
    raise ValueError("Version must have two dots (e.g., '1.0.0').")


def has_only_digits(version: str) -> str:
    """
    Validate that all parts of the version string are numeric.

    Parameters
    ----------
    version : str
        The version string to validate.

    Returns
    -------
    str
        The version string if it is valid.

    Raises
    ------
    ValueError
        If any part of the version string is not numeric.
    """
    pattern = r"[^0-9.]"
    if not re.search(pattern, version):
        return version
    raise ValueError("Version parts must be numeric.")


def validate_version(version: str) -> str:
    """
    Validate that the version string follows semantic versioning (e.g., '1.0.0').

    Parameters
    ----------
    version : str
        The version string to validate.

    Returns
    -------
    str
        The validated version string.

    Raises
    ------
    ValueError
        If the version string does not follow semantic versioning.
    """
    has_two_dots(version)
    has_only_digits(version)
    return version


def validate_pattern(password: str, pattern: str, error_message: str) -> str:
    """
    Validate that the password matches a given regex pattern.

    Parameters
    ----------
    password : str
        The password string to validate.
    pattern : str
        The regex pattern the password must match.
    error_message : str
        The error message to raise if validation fails.

    Returns
    -------
    str
        The validated password string.

    Raises
    ------
    ValueError
        If the password does not match the given pattern.
    """
    compiled_pattern = re.compile(pattern)
    if compiled_pattern.search(password):
        return password
    raise ValueError(error_message)


def validate_password(password: str) -> str:
    """
    Validate that the password meets complexity requirements.

    Parameters
    ----------
    password : str
        The password string to validate.

    Returns
    -------
    str
        The validated password string.

    Raises
    ------
    ValueError
        If the password does not meet complexity requirements.
    """
    validate_pattern(
        password,
        r"[0-9]",
        "Password must contain at least one digit.",
    )
    validate_pattern(
        password,
        r"[A-Z]",
        "Password must contain at least one uppercase letter.",
    )
    validate_pattern(
        password,
        r"[a-z]",
        "Password must contain at least one lowercase letter.",
    )
    validate_pattern(
        password,
        r"[^A-Za-z0-9]",
        "Password must contain at least one special character.",
    )
    return password


def validate_role(
    role: str,
    allowed_roles: Optional[Iterable[Role] | Literal["all", "a", "au"]] = "a",
) -> None:
    """
    Validate that the role is within the allowed roles.

    Parameters
    ----------
    role : str
        The role string to validate.
    allowed_roles : list[Role], Literal["all", "a", "au"], optional
        The list of allowed roles, by default [Role.ADMIN].
        "all" allows all roles. "a" allows only Admin role.
        "au" allows Admin and User roles.

    Raises
    ------
    ValueError
        If the role is not within the allowed roles.
    """

    # Default: admin-only
    if allowed_roles is None:
        allowed_roles = {Role.ADMIN}

    # Expand shorthands
    if allowed_roles == "all":
        allowed_roles = {Role.PUBLIC, Role.USER, Role.ADMIN}
    elif allowed_roles == "a":
        allowed_roles = {Role.ADMIN}
    elif allowed_roles == "au":
        allowed_roles = {Role.ADMIN, Role.USER}

    # Parse role
    try:
        role_enum = Role(role)
    except ValueError:
        raise errors.UnauthorizedError

    # Authorization check
    if role_enum not in allowed_roles:
        if role_enum is Role.PUBLIC:
            raise errors.UnauthorizedError
        raise errors.ForbiddenAccessError
