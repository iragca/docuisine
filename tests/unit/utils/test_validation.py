from fastapi import HTTPException
import pytest
from pytest import raises

from docuisine.schemas.enums import Role
from docuisine.utils.validation import (
    has_only_digits,
    has_two_dots,
    validate_password,
    validate_pattern,
    validate_role,
    validate_version,
)


def test_has_two_dots_valid():
    ## No validation errors should be raised
    assert has_two_dots("1.0.0")
    assert has_two_dots("10.20.30")


def test_has_two_dots_invalid():
    ## Validation errors should be raised
    with raises(ValueError, match="Version must have two dots"):
        has_two_dots("1.0")
    with raises(ValueError, match="Version must have two dots"):
        has_two_dots("1.0.1.1")


def test_has_only_digits_valid():
    ## No validation errors should be raised
    assert has_only_digits("1.0.0")
    assert has_only_digits("10.20.30")


def test_has_only_digits_invalid():
    ## Validation errors should be raised
    with raises(ValueError, match="Version parts must be numeric"):
        has_only_digits("1.a.0")
    with raises(ValueError, match="Version parts must be numeric"):
        has_only_digits("1.0.b")


def test_validate_version_valid():
    ## No validation errors should be raised
    assert validate_version("1.0.0") == "1.0.0"
    assert validate_version("10.20.30") == "10.20.30"


def test_validate_version_invalid():
    ## Validation errors should be raised
    with raises(ValueError, match="Version must have two dots"):
        validate_version("1.0")
    with raises(ValueError, match="Version parts must be numeric"):
        validate_version("1.a.0")


def test_validate_password_valid():
    ## No validation errors should be raised
    assert validate_password("Password1!")
    assert validate_password("A1b2c3d4$")


def test_validate_password_invalid():
    ## Validation errors should be raised
    with raises(ValueError, match="Password must contain at least one digit"):
        validate_password("Password")
    with raises(ValueError, match="Password must contain at least one uppercase letter"):
        validate_password("password1")


def test_validate_pattern_valid():
    ## No validation errors should be raised
    assert validate_pattern("abc123", r"[a-z0-9]", error_message="Invalid pattern")
    assert validate_pattern("TEST_456", r"[A-Z0-9_]", error_message="Invalid pattern")


def test_validate_pattern_invalid():
    ## Validation errors should be raised
    with raises(ValueError, match="Invalid pattern"):
        validate_pattern("abc-123", r"^[a-z0-9]+$", error_message="Invalid pattern")
    with raises(ValueError, match="Invalid pattern"):
        validate_pattern("test@456", r"^[A-Z0-9_]+$", error_message="Invalid pattern")


@pytest.mark.parametrize(
    "role, allowed_roles, should_raise",
    [
        (Role.ADMIN, [Role.ADMIN], False),
        (Role.USER, [Role.ADMIN], True),
        (Role.PUBLIC, [Role.ADMIN, Role.USER], True),
        (Role.USER, [Role.USER, Role.PUBLIC], False),
        (Role.PUBLIC, "all", False),
        (Role.ADMIN, "all", False),
        (Role.USER, None, True),
        (Role.ADMIN, None, False),
        (Role.PUBLIC, "a", True),
        (Role.USER, "a", True),
        (Role.ADMIN, "au", False),
        (Role.PUBLIC, "au", True),
        (None, "au", True),
        ("public", "au", True),
        ("admin", "a", False),
        ("invalid_role", "a", True),
        (None, None, True),
        ("user", "a", True),
    ],
)
def test_validate_role(role, allowed_roles, should_raise):
    if should_raise:
        with raises(HTTPException):
            validate_role(role, allowed_roles)
    else:
        validate_role(role, allowed_roles)  # Should not raise
