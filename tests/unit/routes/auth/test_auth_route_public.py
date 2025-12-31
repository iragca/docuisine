from typing import Callable
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import User
from docuisine.dependencies import services
from docuisine.schemas import Role
from docuisine.utils import errors

from . import params as p


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.POST_PARAMETERS
)
class TestPOST:
    def test_create_token(
        self,
        scenario: str,
        client_name: Role,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        ## Setup
        mock_user_service = MagicMock()

        match scenario:
            case "success_auth":
                mock_user_service.authenticate_user.return_value = User(
                    id=1,
                    username="testuser",
                    email="123@example.com",
                    password="hashedpassword",
                    role="user",
                )
                mock_user_service.create_access_token.return_value = "testaccesstoken"
            case "invalid_credentials":
                mock_user_service.authenticate_user.side_effect = errors.InvalidPasswordError
            case "user_not_found":
                mock_user_service.authenticate_user.side_effect = errors.UserNotFoundError(
                    username="nonexistentuser"
                )

        client = create_client(client_name)
        client.app.dependency_overrides[services.get_user_service] = (  # type: ignore
            lambda: mock_user_service
        )

        ## Test
        response = client.post(
            "/auth/token",
            data={"username": "testuser", "password": "testpassword"},
        )
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response
