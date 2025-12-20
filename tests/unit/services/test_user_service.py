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

    with pytest.raises(ValueError, match="Either user ID or username must be provided."):
        service.get_user()


def test_get_user_by_id(db_session):
    user = User(id=1, username="alice", password="pw")
    db_session.first.return_value = user

    service = UserService(db_session)
    result = service._get_user_by_id(user_id=1)

    db_session.query.assert_called_once_with(User)
    db_session.filter_by.assert_called_with(id=1)
    db_session.first.assert_called_once()
    assert result is user


def test_get_user_by_username(db_session):
    user = User(id=1, username="alice", password="pw")
    db_session.first.return_value = user

    service = UserService(db_session)
    result = service._get_user_by_username(username="alice")

    db_session.query.assert_called_once_with(User)
    db_session.filter_by.assert_called_with(username="alice")
    db_session.first.assert_called_once()
    assert result is user


def test_get_user_not_found_by_id(db_session):
    db_session.first.return_value = None
    service = UserService(db_session)

    with pytest.raises(UserNotFoundError):
        service.get_user(user_id=999)


def test_get_user_not_found_by_username(db_session):
    db_session.first.return_value = None
    service = UserService(db_session)

    with pytest.raises(UserNotFoundError):
        service.get_user(username="nonexistent")


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


def test_delete_user_success(db_session):
    user = User(id=1, username="alice", password="pw")
    db_session.first.return_value = user

    service = UserService(db_session)
    service.delete_user(user_id=1)

    db_session.delete.assert_called_once_with(user)
    db_session.commit.assert_called_once()


def test_delete_user_not_found(db_session):
    db_session.first.return_value = None
    service = UserService(db_session)

    with pytest.raises(UserNotFoundError):
        service.delete_user(user_id=999)


def test_update_email_success(db_session):
    user = User(id=1, username="alice", password="pw", email="old@example.com")
    db_session.first.return_value = user

    service = UserService(db_session)
    updated_user = service.update_user_email(user_id=1, new_email="new@example.com")

    assert updated_user.email == "new@example.com"
    db_session.commit.assert_called_once()


def test_update_email_user_not_found(db_session):
    db_session.first.return_value = None
    service = UserService(db_session)

    with pytest.raises(UserNotFoundError):
        service.update_user_email(user_id=999, new_email="new@example.com")


def test_update_password_success(db_session):
    user = User(id=1, username="alice", password="old_hashed_pw")
    db_session.first.return_value = user

    service = UserService(db_session)
    updated_user = service.update_user_password(user_id=1, new_password="newpassword123")

    assert updated_user.password == "hashed::newpassword123"
    db_session.commit.assert_called_once()


def test_update_password_user_not_found(db_session):
    db_session.first.return_value = None
    service = UserService(db_session)

    with pytest.raises(UserNotFoundError):
        service.update_user_password(user_id=999, new_password="newpassword123")
