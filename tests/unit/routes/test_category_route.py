from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient

from docuisine.db.models import Category
from docuisine.dependencies.services import get_category_service
from docuisine.main import app
from docuisine.utils import errors


class TestPublic:
    def test_get_categories(self):
        """Test getting all categories."""

        def mock_category_service():
            mock = MagicMock()
            mock_categories = [
                Category(id=1, name="Dessert", description="Sweet treats"),
                Category(id=2, name="Vegetarian", description="Plant-based dishes"),
                Category(id=3, name="Quick Meals", description=None),
            ]
            mock.get_all_categories.return_value = mock_categories
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app)

        response = client.get("/categories/")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "Dessert"
        assert data[0]["description"] == "Sweet treats"
        assert data[1]["name"] == "Vegetarian"
        assert data[2]["name"] == "Quick Meals"
        assert data[2]["description"] is None
        assert all("id" in category for category in data)

    def test_get_category_by_id(self):
        """Test getting a category by ID."""

        def mock_category_service():
            mock = MagicMock()
            mock.get_category.return_value = Category(
                id=1, name="Italian", description="Italian cuisine"
            )
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app)

        response = client.get("/categories/1")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Italian"
        assert data["description"] == "Italian cuisine"

    def test_get_category_not_found(self):
        """Test getting a non-existent category returns 404."""

        def mock_category_service():
            mock = MagicMock()
            mock.get_category.side_effect = errors.CategoryNotFoundError(category_id=999)
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app)

        response = client.get("/categories/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Category with ID 999 not found."


class TestAdminUser:
    def test_create_category_success(self, app_admin: MagicMock):
        """Test creating a new category successfully."""

        def mock_category_service():
            mock = MagicMock()
            mock.create_category.return_value = Category(
                id=1, name="Mexican", description="Mexican cuisine"
            )
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        category_data = {"name": "Mexican", "description": "Mexican cuisine"}
        response = client.post("/categories/", json=category_data)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["name"] == "Mexican"
        assert data["description"] == "Mexican cuisine"
        assert data["id"] == 1

    def test_create_category_without_description(self, app_admin: MagicMock):
        """Test creating a category without description."""

        def mock_category_service():
            mock = MagicMock()
            mock.create_category.return_value = Category(id=2, name="Vegan", description=None)
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        category_data = {"name": "Vegan"}
        response = client.post("/categories/", json=category_data)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["name"] == "Vegan"
        assert data["description"] is None

    def test_create_category_conflict(self, app_admin: MagicMock):
        """Test creating a category with duplicate name returns 409."""

        def mock_category_service():
            mock = MagicMock()
            mock.create_category.side_effect = errors.CategoryExistsError(name="Dessert")
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        category_data = {"name": "Dessert", "description": "Sweet dishes"}
        response = client.post("/categories/", json=category_data)
        assert response.status_code == status.HTTP_409_CONFLICT, response.text
        data = response.json()
        assert data["detail"] == "Category with name 'Dessert' already exists."

    def test_update_category_success(self, app_admin: MagicMock):
        """Test updating a category successfully."""

        def mock_category_service():
            mock = MagicMock()
            mock.update_category.return_value = Category(
                id=1, name="Desserts", description="Updated description"
            )
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        update_data = {"name": "Desserts", "description": "Updated description"}
        response = client.put("/categories/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Desserts"
        assert data["description"] == "Updated description"

    def test_update_category_partial(self, app_admin: MagicMock):
        """Test updating only name or description."""

        def mock_category_service():
            mock = MagicMock()
            mock.update_category.return_value = Category(
                id=1, name="Updated Name", description="Original description"
            )
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        update_data = {"name": "Updated Name"}
        response = client.put("/categories/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_update_category_not_found(self, app_admin: MagicMock):
        """Test updating a non-existent category returns 404."""

        def mock_category_service():
            mock = MagicMock()
            mock.update_category.side_effect = errors.CategoryNotFoundError(category_id=999)
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        update_data = {"name": "New Name"}
        response = client.put("/categories/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Category with ID 999 not found."

    def test_update_category_conflict(self, app_admin: MagicMock):
        """Test updating to a duplicate name returns 409."""

        def mock_category_service():
            mock = MagicMock()
            mock.update_category.side_effect = errors.CategoryExistsError(name="Existing")
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        update_data = {"name": "Existing"}
        response = client.put("/categories/1", json=update_data)
        assert response.status_code == status.HTTP_409_CONFLICT, response.text
        data = response.json()
        assert data["detail"] == "Category with name 'Existing' already exists."

    def test_delete_category_success(self, app_admin: MagicMock):
        """Test deleting a category successfully."""

        def mock_category_service():
            mock = MagicMock()
            mock.delete_category.return_value = None
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        response = client.delete("/categories/1")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["detail"] == "Category with ID 1 has been deleted."

    def test_delete_category_not_found(self, app_admin: MagicMock):
        """Test deleting a non-existent category returns 404."""

        def mock_category_service():
            mock = MagicMock()
            mock.delete_category.side_effect = errors.CategoryNotFoundError(category_id=999)
            return mock

        app.dependency_overrides[get_category_service] = mock_category_service
        client = TestClient(app_admin)

        response = client.delete("/categories/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Category with ID 999 not found."
