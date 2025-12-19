from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from docuisine.db.models import User
from docuisine.services.user import UserService
from docuisine.utils.errors import UserExistsError, UserNotFoundError


@pytest.fixture
def db_session():
    session = MagicMock()
    session.query.return_value = session
    session.filter_by.return_value = session
    return session


@pytest.fixture(autouse=True)
def mock_hash(monkeypatch):
    monkeypatch.setattr(
        "docuisine.services.user.hash_in_sha256",
        lambda pw: f"hashed::{pw}",
    )


def test_create_user_success(db_session):
    service = UserService(db_session)

    user = service.create_user("alice", "password123")

    assert isinstance(user, User)
    assert user.username == "alice"
    assert user.password == "hashed::password123"

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()


def test_create_user_duplicate_raises(db_session):
    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )

    service = UserService(db_session)

    with pytest.raises(UserExistsError) as exc:
        service.create_user("alice", "password123")

    assert "alice" in str(exc.value)
    db_session.rollback.assert_called_once()


def test_get_user_no_args_raises(db_session):
    service = UserService(db_session)

    with pytest.raises(ValueError):
        service.get_user()


def test_get_user_by_id(db_session):
    user = User(id=1, username="alice", password="pw")
    db_session.first.return_value = user

    service = UserService(db_session)
    result = service.get_user(user_id=1)

    assert result is user
    db_session.filter_by.assert_called_with(id=1)


def test_get_user_by_username(db_session):
    user = User(id=1, username="alice", password="pw")
    db_session.first.return_value = user

    service = UserService(db_session)
    result = service.get_user(username="alice")

    assert result is user
    db_session.filter_by.assert_called_with(username="alice")


def test_get_user_not_found_by_id(db_session):
    db_session.first.return_value = None
    service = UserService(db_session)

    with pytest.raises(UserNotFoundError):
        service.get_user(user_id=999)


def test_get_all_users(db_session):
    users = [
        User(id=1, username="alice", password="pw"),
        User(id=2, username="bob", password="pw"),
    ]
    db_session.all.return_value = users

    service = UserService(db_session)
    result = service.get_all_users()

    assert result == users
    db_session.query.assert_called_once_with(User)


def test_create_user_with_email(db_session):
    service = UserService(db_session)

    user = service.create_user("alice", "password123", email="alice@example.com")

    assert isinstance(user, User)
    assert user.username == "alice"
    assert user.password == "hashed::password123"
    assert user.email == "alice@example.com"

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
