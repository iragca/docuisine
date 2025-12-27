from fastapi import status
from fastapi.testclient import TestClient
import pytest


class TestGET:
    @pytest.mark.parametrize(
        "client, expected_status",
        [
            ("public_client", status.HTTP_200_OK),
            ("user_client", status.HTTP_200_OK),
            ("admin_client", status.HTTP_200_OK),
        ],
        indirect=["client"],
        ids=["public", "user", "admin"],
    )
    def test_root_route(self, client: TestClient, expected_status: int):
        """Test the public root route returns status 200 and correct message."""
        response = client.get("/")
        assert response.status_code == expected_status, response.text
        assert response.json() == "Hello, from Docuisine!"
