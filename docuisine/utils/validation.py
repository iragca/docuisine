import re


def has_two_dots(version: str) -> bool:
    """
    Validate that the version string has exactly two dots.

    Parameters
    ----------
    version : str
        The version string to validate.

    Returns
    -------
    bool
        True if the version string is valid.

    Raises
    ------
    ValueError
        If the version string does not have exactly two dots.
    """
    if version.count(".") == 2:
        return True
    raise ValueError("Version must have two dots (e.g., '1.0.0').")


def has_only_digits(version: str) -> bool:
    """
    Validate that all parts of the version string are numeric.

    Parameters
    ----------
    version : str
        The version string to validate.

    Returns
    -------
    bool
        True if the version string is valid.

    Raises
    ------
    ValueError
        If any part of the version string is not numeric.
    """
    if all(part.isdigit() for part in version.split(".")):
        return True
    raise ValueError("Version parts must be numeric.")


def at_least_one_digit(password: str) -> bool:
    """
    Validate that the password contains at least one digit.
    Parameters
    ----------
    password : str
        The password string to validate.

    Returns
    -------
    bool
        True if the password is valid.
    Raises
    ------
    ValueError
        If the password does not contain at least one digit.
    """

    if any(char.isdigit() for char in password):
        return True
    raise ValueError("Password must contain at least one digit.")


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


def validate_pattern(password: str, pattern: str, error_message: str) -> bool:
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
    bool
        True if the password is valid.

    Raises
    ------
    ValueError
        If the password does not match the given pattern.
    """
    compiled_pattern = re.compile(pattern)
    if compiled_pattern.search(password):
        return True
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
