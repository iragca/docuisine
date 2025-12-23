from unittest.mock import MagicMock

from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import User
from docuisine.dependencies.auth import get_client_user
from docuisine.dependencies.services import get_user_service
from docuisine.main import app


@pytest.fixture(scope="module")
def mock_user_service():
    """
    Provide a mock UserService.
    Used in units test for routes by mocking the services.
    """
    mock = MagicMock()
    return mock


@pytest.fixture(scope="module")
def client(mock_user_service):
    """
    Provide a TestClient with mocked dependencies.
    Used in units test for routes by mocking the services with a test client.
    """
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    yield TestClient(app)
    app.dependency_overrides.clear()


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
    """
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = "dev-user"
    mock_user.password = "hashed::DevPassword1P!"
    mock_user.email = "dev-user@docuisine.org"
    mock_user.role = "user"
    return mock_user

@pytest.fixture
def app_regular_user(regular_user):
    """
    Provide a TestClient with a regular authenticated user.
    Used in unit tests for routes that require an authenticated regular user.
    """
    app.dependency_overrides[get_client_user] = lambda: regular_user
    return app


@pytest.fixture
def admin_user():
    """
    Provide an admin user instance for testing.
    Used in unit tests for services and routes that require an admin user.
    """
    mock_user = MagicMock(spec=User)
    mock_user.id = 2
    mock_user.username = "dev-admin"
    mock_user.password = "hashed::DevPassword2P!"
    mock_user.email = "dev-admin@docuisine.org"
    mock_user.role = "admin"
    return mock_user

@pytest.fixture
def app_admin(admin_user):
    """
    Provide a TestClient with an admin authenticated user.
    Used in unit tests for routes that require an authenticated admin user.
    """
    app.dependency_overrides[get_client_user] = lambda: admin_user
    return app
