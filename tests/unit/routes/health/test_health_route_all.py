from typing import Callable

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from docuisine.schemas.enums import Role


class TestGET:
    @pytest.mark.parametrize(
        "client_name, expected_status",
        [
            ("public", status.HTTP_200_OK),
            ("user", status.HTTP_200_OK),
            ("admin", status.HTTP_200_OK),
        ],
    )
    def test_health_route(
        self,
        client_name: str,
        expected_status: int,
        create_client: Callable[[Role | str], TestClient],
    ):
        """Test the public health route with admin user authentication returns status 200 and correct message."""
        response = create_client(client_name).get("/health/")
        assert response.status_code == expected_status, response.text
        data = response.json()
        assert data["status"] == "healthy"
        assert "commit_hash" in data
        assert "version" in data
