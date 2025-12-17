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
