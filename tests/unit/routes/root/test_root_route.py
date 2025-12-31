from typing import Callable

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from docuisine.schemas.enums import Role


class TestGET:
    @pytest.mark.parametrize(
        "client_name, expected_status",
        [
            (Role.PUBLIC, status.HTTP_200_OK),
            (Role.USER, status.HTTP_200_OK),
            (Role.ADMIN, status.HTTP_200_OK),
        ],
    )
    def test_root_route(
        self, client_name: str, expected_status: int, create_client: Callable[[str], TestClient]
    ):
        """Test the public root route returns status 200 and correct message."""
        client = create_client(client_name)
        response = client.get("/")
        assert response.status_code == expected_status, response.text
        assert response.json() == "Hello, from Docuisine!"
