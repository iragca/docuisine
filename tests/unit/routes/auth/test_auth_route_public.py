from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient

from docuisine.db.models import User
from docuisine.dependencies import services
from docuisine.utils import errors


class TestPOST:
    def test_create_token(self, public_client: TestClient):
        ## Setup
        mock_user_service = MagicMock()
        mock_user_service.authenticate_user.return_value = User(
            id=1,
            username="testuser",
            email="123@example.com",
            password="hashedpassword",
            role="user",
        )
        mock_user_service.create_access_token.return_value = "testaccesstoken"
        public_client.app.dependency_overrides[services.get_user_service] = (  # type: ignore
            lambda: mock_user_service
        )

        ## Test
        response = public_client.post(
            "/auth/token",
            data={"username": "testuser", "password": "testpassword"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["access_token"] == "testaccesstoken"

    def test_invalid_credentials(self, public_client: TestClient):
        ## Setup
        mock_user_service = MagicMock()
        mock_user_service.authenticate_user.side_effect = errors.InvalidPasswordError
        public_client.app.dependency_overrides[services.get_user_service] = (  # type: ignore
            lambda: mock_user_service
        )

        ## Test
        response = public_client.post(
            "/auth/token",
            data={"username": "invaliduser", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "The provided password is invalid."

    def test_user_not_found(self, public_client: TestClient):
        ## Setup
        mock_user_service = MagicMock()
        mock_user_service.authenticate_user.side_effect = errors.UserNotFoundError(
            username="nonexistentuser"
        )
        public_client.app.dependency_overrides[services.get_user_service] = (  # type: ignore
            lambda: mock_user_service
        )

        ## Test
        response = public_client.post(
            "/auth/token",
            data={"username": "nonexistentuser", "password": "somepassword"},
        )
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "User with username 'nonexistentuser' not found."
