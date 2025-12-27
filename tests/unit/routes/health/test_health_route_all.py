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
    def test_health_route(self, client: TestClient, expected_status: int):
        """Test the public health route with admin user authentication returns status 200 and correct message."""
        response = client.get("/health")
        assert response.status_code == expected_status, response.text
        data = response.json()
        assert data["status"] == "healthy"
        assert "commit_hash" in data
        assert "version" in data
