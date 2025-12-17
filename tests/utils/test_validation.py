from pytest import raises

from docuisine.utils.validation import (
    at_least_one_digit,
    has_only_digits,
    has_two_dots,
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


def test_at_least_one_digit_valid():
    ## No validation errors should be raised
    assert at_least_one_digit("password1")
    assert at_least_one_digit("12345")


def test_at_least_one_digit_invalid():
    ## Validation errors should be raised
    with raises(ValueError, match="Password must contain at least one digit"):
        at_least_one_digit("password")
    with raises(ValueError, match="Password must contain at least one digit"):
        at_least_one_digit("nopasswordhere")
