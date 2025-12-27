from fastapi import status
from fastapi.testclient import TestClient


class TestGET:
    def test_health_route_admin(self, admin_client: TestClient):
        """Test the public health route with admin user authentication returns status 200 and correct message."""
        response = admin_client.get("/health")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["status"] == "healthy"
        assert "commit_hash" in data
        assert "version" in data
