from fastapi.testclient import TestClient
import pytest

from docuisine.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data.get("status") == "healthy"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello" in response.json()


def test_nonexistent_endpoint(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_add_user(client):
    user_data = {"username": "testuser", "password": "testpass123C$"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_add_existing_user(client):
    user_data = {"username": "existinguser", "password": "Password123!"}
    # First, create the user
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    # Try to create the same user again
    response = client.post("/users/", json=user_data)
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "User with username existinguser already exists."
