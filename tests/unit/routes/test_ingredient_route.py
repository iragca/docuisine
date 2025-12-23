from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient

from docuisine.db.models import Ingredient
from docuisine.dependencies.services import get_ingredient_service
from docuisine.main import app
from docuisine.utils import errors


class TestPublic:
    def test_get_ingredients(self):
        """Test getting all ingredients."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock_ingredients = [
                Ingredient(id=1, name="Sugar", description="White sugar", recipe_id=None),
                Ingredient(id=2, name="Flour", description="All-purpose flour", recipe_id=None),
                Ingredient(id=3, name="Salt", description=None, recipe_id=None),
            ]
            mock.get_all_ingredients.return_value = mock_ingredients
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app)

        response = client.get("/ingredients/")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "Sugar"
        assert data[0]["description"] == "White sugar"
        assert data[1]["name"] == "Flour"
        assert data[2]["name"] == "Salt"
        assert data[2]["description"] is None
        assert all("id" in ingredient for ingredient in data)

    def test_get_ingredient_by_id(self):
        """Test getting an ingredient by ID."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.get_ingredient.return_value = Ingredient(
                id=1, name="Butter", description="Unsalted butter", recipe_id=None
            )
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app)

        response = client.get("/ingredients/1")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Butter"
        assert data["description"] == "Unsalted butter"
        assert data["recipe_id"] is None

    def test_get_ingredient_not_found(self):
        """Test getting a non-existent ingredient returns 404."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.get_ingredient.side_effect = errors.IngredientNotFoundError(ingredient_id=999)
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app)

        response = client.get("/ingredients/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Ingredient with ID 999 not found."


class TestRegularUser:
    def test_create_ingredient_success(self, app_regular_user: MagicMock):
        """Test creating a new ingredient successfully."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.create_ingredient.return_value = Ingredient(
                id=1, name="Eggs", description="Large eggs", recipe_id=None
            )
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app)

        ingredient_data = {"name": "Eggs", "description": "Large eggs"}
        response = client.post("/ingredients/", json=ingredient_data)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["name"] == "Eggs"
        assert data["description"] == "Large eggs"
        assert data["id"] == 1
        assert data["recipe_id"] is None

    def test_create_ingredient_without_description(self, app_regular_user: MagicMock):
        """Test creating an ingredient without description."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.create_ingredient.return_value = Ingredient(
                id=2, name="Pepper", description=None, recipe_id=None
            )
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_regular_user)

        ingredient_data = {"name": "Pepper"}
        response = client.post("/ingredients/", json=ingredient_data)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["name"] == "Pepper"
        assert data["description"] is None

    def test_create_ingredient_with_recipe_id(self, app_regular_user: MagicMock):
        """Test creating an ingredient with a recipe_id."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.create_ingredient.return_value = Ingredient(
                id=3, name="Pasta", description="Homemade pasta", recipe_id=5
            )
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_regular_user)

        ingredient_data = {"name": "Pasta", "description": "Homemade pasta", "recipe_id": 5}
        response = client.post("/ingredients/", json=ingredient_data)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["name"] == "Pasta"
        assert data["recipe_id"] == 5

    def test_create_ingredient_conflict(self, app_regular_user: MagicMock):
        """Test creating an ingredient with duplicate name returns 409."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.create_ingredient.side_effect = errors.IngredientExistsError(name="Sugar")
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_regular_user)

        ingredient_data = {"name": "Sugar", "description": "White sugar"}
        response = client.post("/ingredients/", json=ingredient_data)
        assert response.status_code == status.HTTP_409_CONFLICT, response.text
        data = response.json()
        assert data["detail"] == "Ingredient with name 'Sugar' already exists."


class TestAdminUser:
    def test_update_ingredient_success(self, app_regular_user: MagicMock):
        """Test updating an ingredient successfully."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.update_ingredient.return_value = Ingredient(
                id=1, name="Brown Sugar", description="Updated description", recipe_id=None
            )
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_regular_user)

        update_data = {"name": "Brown Sugar", "description": "Updated description"}
        response = client.put("/ingredients/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Brown Sugar"
        assert data["description"] == "Updated description"

    def test_update_ingredient_partial(self, app_regular_user: MagicMock):
        """Test updating only name or description."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.update_ingredient.return_value = Ingredient(
                id=1, name="Updated Name", description="Original description", recipe_id=None
            )
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_regular_user)

        update_data = {"name": "Updated Name"}
        response = client.put("/ingredients/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_update_ingredient_recipe_id(self, app_admin: MagicMock):
        """Test updating ingredient's recipe_id."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.update_ingredient.return_value = Ingredient(
                id=1, name="Dough", description="Pizza dough", recipe_id=10
            )
            return mock

        app_admin.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_admin)

        update_data = {"recipe_id": 10}
        response = client.put("/ingredients/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["recipe_id"] == 10

    def test_update_ingredient_not_found(self, app_admin: MagicMock):
        """Test updating a non-existent ingredient returns 404."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.update_ingredient.side_effect = errors.IngredientNotFoundError(ingredient_id=999)
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_admin)

        update_data = {"name": "New Name"}
        response = client.put("/ingredients/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Ingredient with ID 999 not found."

    def test_update_ingredient_conflict(self, app_admin: MagicMock):
        """Test updating to a duplicate name returns 409."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.update_ingredient.side_effect = errors.IngredientExistsError(name="Existing")
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_admin)

        update_data = {"name": "Existing"}
        response = client.put("/ingredients/1", json=update_data)
        assert response.status_code == status.HTTP_409_CONFLICT, response.text
        data = response.json()
        assert data["detail"] == "Ingredient with name 'Existing' already exists."

    def test_delete_ingredient_success(self, app_admin: MagicMock):
        """Test deleting an ingredient successfully."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.delete_ingredient.return_value = None
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_admin)

        response = client.delete("/ingredients/1")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["detail"] == "Ingredient with ID 1 has been deleted."

    def test_delete_ingredient_not_found(self, app_admin: MagicMock):
        """Test deleting a non-existent ingredient returns 404."""

        def mock_ingredient_service():
            mock = MagicMock()
            mock.delete_ingredient.side_effect = errors.IngredientNotFoundError(ingredient_id=999)
            return mock

        app.dependency_overrides[get_ingredient_service] = mock_ingredient_service
        client = TestClient(app_admin)

        response = client.delete("/ingredients/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Ingredient with ID 999 not found."
