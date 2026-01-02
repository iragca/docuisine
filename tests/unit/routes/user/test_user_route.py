from typing import Callable
from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import User
from docuisine.dependencies.services import get_user_service
from docuisine.schemas import Role
from docuisine.utils import errors

from . import params as p


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.GET_PARAMETERS
)
class TestGET:
    def test_get_user(
        self,
        scenario: str,
        client_name: Role,
        expected_status: int,
        expected_response: dict | list,
        create_client: Callable[[Role], TestClient],
    ):
        """Test GET routes for all scenarios (all users, not found)."""

        def mock_user_service():
            mock = MagicMock()
            if scenario == "get_all":
                mock.get_all_users.return_value = [
                    User(**user) for user in p.GET_ALL_USERS_RESPONSE
                ]
            elif scenario == "get_not_found":
                mock.get_user.side_effect = errors.UserNotFoundError(user_id=999)
            elif scenario == "get_existing":
                mock.get_user.return_value = User(**p.GET_A_USER_RESPONSE)
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_user_service] = mock_user_service  # type: ignore

        # Make the request
        if scenario == "get_all":
            response = client.get("/users/")
        elif scenario == "get_not_found":
            response = client.get("/users/999")
        elif scenario == "get_existing":
            response = client.get("/users/user3")

        # Assertions
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


class TestPOST:
    @pytest.mark.parametrize(
        "client_name, expected_status, expected_response",
        p.POST_PARAMETERS,
    )
    def test_create_user(
        self,
        client_name: Role,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test creating a new user."""

        def mock_user_service():
            mock = MagicMock()
            match expected_status:
                case status.HTTP_201_CREATED:
                    mock.create_user.return_value = User(**expected_response)
                case status.HTTP_409_CONFLICT:
                    mock.create_user.side_effect = errors.UserExistsError(username="user1")
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_user_service] = (  # type: ignore
            mock_user_service
        )

        user_data = {
            "username": "newuser",
            "password": "SomePassword!23",
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == expected_status, response.text
        data = response.json()
        assert data == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, input_data, expected_status, expected_response", p.PUT_PARAMETERS
)
class TestPUT:
    def test_update_user(
        self,
        scenario: str,
        client_name: Role,
        input_data: dict,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test updating users with various scenarios."""

        def mock_user_service():
            mock = MagicMock()
            if scenario == "update_password_success":
                mock.update_user_password.return_value = User(**expected_response)
            elif scenario == "update_password_not_found":
                mock.update_user_password.side_effect = errors.UserNotFoundError(user_id=1)
            elif scenario == "update_email_success":
                mock.update_user_email.return_value = User(**expected_response)
            elif scenario == "update_email_not_found":
                mock.update_user_email.side_effect = errors.UserNotFoundError(user_id=1)
            elif scenario == "update_email_conflict":
                mock.update_user_email.side_effect = errors.DuplicateEmailError(
                    email="newemail@example.com"
                )
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_user_service] = mock_user_service  # type: ignore

        # Route depends on scenario
        if "password" in scenario:
            response = client.put("/users/password", json=input_data)
        elif "email" in scenario:
            response = client.put("/users/email", json=input_data)

        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, user_id, expected_status, expected_response", p.DELETE_PARAMETERS
)
class TestDELETE:
    def test_delete_user(
        self,
        scenario: str,
        client_name: Role,
        user_id: int,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test deleting users with various scenarios."""

        def mock_user_service():
            mock = MagicMock()
            if scenario == "delete_success":
                mock.delete_user.return_value = None
            elif scenario == "delete_not_found":
                mock.delete_user.side_effect = errors.UserNotFoundError(user_id=user_id)
            elif scenario == "unauthorized":
                mock.delete_user.side_effect = errors.ForbiddenAccessError
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_user_service] = mock_user_service  # type: ignore

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response
