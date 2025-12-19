from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient

from docuisine.db.models import User
from docuisine.dependencies.services import get_user_service
from docuisine.main import app
from docuisine.utils import errors


def test_get_users():
    ## Setup
    def mock_user_service():
        mock = MagicMock()
        mock_users = [
            User(id=1, username="user1", password="Password!hashed1"),
            User(id=2, username="user2", password="Password!hashed2"),
        ]
        mock.get_all_users.return_value = mock_users

        return mock

    app.dependency_overrides[get_user_service] = mock_user_service
    client = TestClient(app)

    ## Test
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "user1"
    assert data[1]["username"] == "user2"
    assert "id" in data[0]
    assert "id" in data[1]

    assert all("password" not in user for user in data)  # Ensure passwords are not exposed


def test_get_user_not_found(client, mock_user_service):
    def mock_user_service():
        mock = MagicMock()
        mock.get_user.side_effect = errors.UserNotFoundError(user_id=999)
        return mock

    app.dependency_overrides[get_user_service] = mock_user_service
    client = TestClient(app)

    response = client.get("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == "User with ID 999 not found."


def test_create_user_conflict(client):
    ## Setup
    def mock_user_service():
        mock = MagicMock()
        mock.create_user.side_effect = errors.UserExistsError(username="user1")
        return mock

    app.dependency_overrides[get_user_service] = mock_user_service
    client = TestClient(app)

    ## Test
    user_data = {
        "username": "user1",
        "password": "SomePassword!23",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "User with username user1 already exists."
