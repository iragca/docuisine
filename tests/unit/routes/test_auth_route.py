from docuisine.db.models import User
from docuisine.utils import errors


def test_create_token(client, mock_user_service):
    ## Setup
    mock_user_service.authenticate_user.return_value = User(
        id=1,
        username="testuser",
        email="123@example.com",
        password="hashedpassword",
        role="user",
    )
    mock_user_service.create_access_token.return_value = "testaccesstoken"

    ## Test
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"] == "testaccesstoken"


def test_invalid_credentials(client, mock_user_service):
    ## Setup
    mock_user_service.authenticate_user.side_effect = errors.InvalidPasswordError

    ## Test
    response = client.post(
        "/auth/token",
        data={"username": "invaliduser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "The provided password is invalid."


def test_user_not_found(client, mock_user_service):
    ## Setup
    mock_user_service.authenticate_user.side_effect = errors.UserNotFoundError(
        username="nonexistentuser"
    )

    ## Test
    response = client.post(
        "/auth/token",
        data={"username": "nonexistentuser", "password": "somepassword"},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User with username 'nonexistentuser' not found."
