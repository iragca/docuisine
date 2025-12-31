from typing import Callable, Union
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import User
from docuisine.dependencies.auth import get_client_user
from docuisine.main import app
from docuisine.schemas.enums import Role


@pytest.fixture
def db_session():
    """
    Provide a mock database session for testing.
    Used in unit tests for services by mocking the database session.
    """
    session = MagicMock()
    session.query.return_value = session
    session.filter_by.return_value = session
    session.delete.return_value = session
    session.commit.return_value = session
    session.add.return_value = session
    session.rollback.return_value = session
    return session


@pytest.fixture
def regular_user():
    """
    Provide a regular user instance for testing.
    Used in unit tests for services and routes that require a regular user.

    NOTES
    -----
    Do not use mock user with MagicMock.
    This will break identity access checks in routes.
    """
    return User(
        id=1,
        username="dev-user",
        password="hashed::DevPassword1P!",
        email="dev-user@docuisine.org",
        role=Role.USER,
    )


@pytest.fixture
def admin_user():
    """
    Provide an admin user instance for testing.
    Used in unit tests for services and routes that require an admin user.

    NOTES
    -----
    Do not use mock user with MagicMock.
    This will break identity access checks in routes.
    """
    return User(
        id=2,
        username="dev-admin",
        password="hashed::DevPassword2P!",
        email="dev-admin@docuisine.org",
        role=Role.ADMIN,
    )


@pytest.fixture
def public_user():
    """
    Provide a public (unauthenticated) pseudo user instance for testing.
    Used in unit tests for services and routes that require no authenticated user.

    NOTES
    -----
    Do not use mock user with MagicMock.
    This will break identity access checks in routes.
    """
    return User(
        id=3,
        username="dev-public",
        password="hashed::DevPassword3P!",
        email="dev-public@docuisine.org",
        role=Role.PUBLIC,
    )


@pytest.fixture
def create_client(
    admin_user: User, regular_user: User, public_user: User
) -> Callable[[Union[Role, str]], TestClient | None]:
    """
    Provide a TestClient factory function based on client role.

    Used in unit tests for routes to create clients with different authenticated user roles.

    Returns
    -------
    Callable[[Union[Role, str]], TestClient | None]
        A factory function that creates TestClient instances for different roles.
        The returned function can raise ValueError if an unknown client_name is provided.
    """

    def client_factory(client_name: Union[Role, str]) -> TestClient | None:
        """
        Setup TestClient based on client role using a client factory.

        Parameters
        ----------
        client_name : Union[Role, str]
            The role of the client to setup (ADMIN, USER, PUBLIC).

        Returns
        -------
        TestClient
            The configured TestClient instance.

        Raises
        ------
        ValueError
            If an unknown `client_name` is provided.
        """
        if isinstance(client_name, str):
            client_name = Role(client_name.lower().strip())

        match client_name:
            case Role.ADMIN:
                app.dependency_overrides[get_client_user] = lambda: admin_user
                return TestClient(app)
            case Role.USER:
                app.dependency_overrides[get_client_user] = lambda: regular_user
                return TestClient(app)
            case Role.PUBLIC:
                app.dependency_overrides[get_client_user] = lambda: public_user
                return TestClient(app)
            case _:
                raise ValueError(f"Unknown client_name: {client_name}")

    return client_factory
