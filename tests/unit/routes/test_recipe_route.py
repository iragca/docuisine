from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient

from docuisine.db.models import Recipe
from docuisine.dependencies.services import get_recipe_service
from docuisine.main import app
from docuisine.utils import errors


class TestPublic:
    def test_get_recipes(self):
        """Test getting all recipes."""

        def mock_recipe_service():
            mock = MagicMock()
            mock_recipes = [
                Recipe(id=1, user_id=1, name="Pasta Carbonara"),
                Recipe(
                    id=2, user_id=1, name="Chicken Curry", prep_time_sec=900, cook_time_sec=1800
                ),
                Recipe(id=3, user_id=2, name="Vegan Tacos", servings=4),
            ]
            mock.get_all_recipes.return_value = mock_recipes
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app)

        response = client.get("/recipes/")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "Pasta Carbonara"
        assert data[0]["user_id"] == 1
        assert data[1]["name"] == "Chicken Curry"
        assert data[1]["prep_time_sec"] == 900
        assert data[1]["cook_time_sec"] == 1800
        assert data[2]["name"] == "Vegan Tacos"
        assert data[2]["servings"] == 4
        assert "id" in data[0] and "id" in data[1]

    def test_get_recipes_by_user(self):
        """Test getting recipes for a specific user."""

        def mock_recipe_service():
            mock = MagicMock()
            mock_recipes = [
                Recipe(id=1, user_id=1, name="Pasta Carbonara"),
                Recipe(id=2, user_id=1, name="Chicken Curry", prep_time_sec=900),
            ]
            mock.get_recipes_by_user.return_value = mock_recipes
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app)

        response = client.get("/recipes/user/1")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert len(data) == 2
        assert all(recipe["user_id"] == 1 for recipe in data)
        assert data[0]["name"] == "Pasta Carbonara"
        assert data[1]["name"] == "Chicken Curry"

    def test_get_recipe_by_id(self):
        """Test getting a recipe by ID."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.get_recipe.return_value = Recipe(
                id=1,
                user_id=1,
                name="Beef Stew",
                prep_time_sec=1200,
                cook_time_sec=7200,
                non_blocking_time_sec=8400,
                servings=6,
            )
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app)

        response = client.get("/recipes/1")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["user_id"] == 1
        assert data["name"] == "Beef Stew"
        assert data["prep_time_sec"] == 1200
        assert data["cook_time_sec"] == 7200
        assert data["non_blocking_time_sec"] == 8400
        assert data["servings"] == 6

    def test_get_recipe_not_found(self):
        """Test getting a non-existent recipe returns 404."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.get_recipe.side_effect = errors.RecipeNotFoundError(recipe_id=999)
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app)

        response = client.get("/recipes/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Recipe with ID 999 not found."


class TestAdminUser:
    def test_create_recipe_success(self, app_admin: MagicMock):
        """Test creating a new recipe successfully."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.create_recipe.return_value = Recipe(
                id=1,
                user_id=1,
                name="Chocolate Cake",
                prep_time_sec=1800,
                cook_time_sec=2700,
                servings=8,
            )
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        recipe_data = {
            "name": "Chocolate Cake",
            "prep_time_sec": 1800,
            "cook_time_sec": 2700,
            "servings": 8,
        }
        response = client.post("/recipes/", json=recipe_data)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["name"] == "Chocolate Cake"
        assert data["user_id"] == 1
        assert data["prep_time_sec"] == 1800
        assert data["cook_time_sec"] == 2700
        assert data["servings"] == 8
        assert data["id"] == 1

    def test_create_recipe_minimal_fields(self, app_admin: MagicMock):
        """Test creating a recipe with only required fields."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.create_recipe.return_value = Recipe(id=2, user_id=2, name="Simple Salad")
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        recipe_data = {"user_id": 2, "name": "Simple Salad"}
        response = client.post("/recipes/", json=recipe_data)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["name"] == "Simple Salad"
        assert data["user_id"] == 2

    def test_create_recipe_conflict(self, app_admin: MagicMock):
        """Test creating a recipe with duplicate name for user returns 409."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.create_recipe.side_effect = errors.RecipeExistsError(name="Existing Recipe")
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        recipe_data = {"user_id": 1, "name": "Existing Recipe"}
        response = client.post("/recipes/", json=recipe_data)
        assert response.status_code == status.HTTP_409_CONFLICT, response.text
        data = response.json()
        assert data["detail"] == "Recipe with name 'Existing Recipe' already exists."

    def test_update_recipe_success(self, app_admin: MagicMock):
        """Test updating a recipe successfully."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.update_recipe.return_value = Recipe(
                id=1,
                user_id=1,
                name="Updated Recipe",
                prep_time_sec=1500,
                cook_time_sec=2400,
                non_blocking_time_sec=3900,
                servings=4,
            )
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        update_data = {
            "name": "Updated Recipe",
            "prep_time_sec": 1500,
            "cook_time_sec": 2400,
            "non_blocking_time_sec": 3900,
            "servings": 4,
        }
        response = client.put("/recipes/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Updated Recipe"
        assert data["prep_time_sec"] == 1500
        assert data["cook_time_sec"] == 2400
        assert data["non_blocking_time_sec"] == 3900
        assert data["servings"] == 4

    def test_update_recipe_partial(self, app_admin: MagicMock):
        """Test updating only some fields."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.update_recipe.return_value = Recipe(
                id=1,
                user_id=1,
                name="Original Name",
                servings=10,
            )
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        update_data = {"servings": 10}
        response = client.put("/recipes/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["servings"] == 10

    def test_update_recipe_not_found(self, app_admin: MagicMock):
        """Test updating a non-existent recipe returns 404."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.update_recipe.side_effect = errors.RecipeNotFoundError(recipe_id=999)
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        update_data = {"name": "New Name"}
        response = client.put("/recipes/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Recipe with ID 999 not found."

    def test_update_recipe_conflict(self, app_admin: MagicMock):
        """Test updating to a duplicate name for user returns 409."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.update_recipe.side_effect = errors.RecipeExistsError(name="Existing Recipe")
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        update_data = {"name": "Existing Recipe"}
        response = client.put("/recipes/1", json=update_data)
        assert response.status_code == status.HTTP_409_CONFLICT, response.text
        data = response.json()
        assert data["detail"] == "Recipe with name 'Existing Recipe' already exists."

    def test_delete_recipe_success(self, app_admin: MagicMock):
        """Test deleting a recipe successfully."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.delete_recipe.return_value = None
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        response = client.delete("/recipes/1")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["detail"] == "Recipe with ID 1 has been deleted."

    def test_delete_recipe_not_found(self, app_admin: MagicMock):
        """Test deleting a non-existent recipe returns 404."""

        def mock_recipe_service():
            mock = MagicMock()
            mock.delete_recipe.side_effect = errors.RecipeNotFoundError(recipe_id=999)
            return mock

        app.dependency_overrides[get_recipe_service] = mock_recipe_service
        client = TestClient(app_admin)

        ## Test
        response = client.delete("/recipes/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        data = response.json()
        assert data["detail"] == "Recipe with ID 999 not found."
