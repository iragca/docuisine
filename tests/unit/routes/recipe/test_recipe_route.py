from typing import Callable
from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import Recipe
from docuisine.dependencies.services import get_recipe_service
from docuisine.schemas import Role
from docuisine.utils import errors

from . import params as p


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.GET_PARAMETERS
)
class TestGET:
    def test_get_recipe(
        self,
        scenario: str,
        client_name: Role,
        expected_status: int,
        expected_response: dict | list,
        create_client: Callable[[Role], TestClient],
    ):
        """Test GET routes for all scenarios (all recipes, by ID, not found)."""

        def mock_recipe_service():
            mock = MagicMock()
            if scenario == "get_all":
                mock.get_all_recipes.return_value = [
                    Recipe(**recipe) for recipe in p.GET_ALL_RECIPES_RESPONSE
                ]
            elif scenario == "get_by_id":
                mock.get_recipe.return_value = Recipe(**p.GET_RECIPE_BY_ID_RESPONSE)
            elif scenario == "get_not_found":
                mock.get_recipe.side_effect = errors.RecipeNotFoundError(recipe_id=999)
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_recipe_service] = mock_recipe_service  # type: ignore

        # Make the request
        if scenario == "get_all":
            response = client.get("/recipes/")
        elif scenario in ["get_by_id", "get_not_found"]:
            response = client.get("/recipes/1" if scenario == "get_by_id" else "/recipes/999")

        # Assertions
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


class TestPOST:
    @pytest.mark.parametrize(
        "client_name, expected_status, expected_response",
        p.POST_PARAMETERS,
    )
    def test_create_recipe(
        self,
        client_name: Role,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test creating a new recipe."""

        def mock_recipe_service():
            mock = MagicMock()
            match expected_status:
                case status.HTTP_201_CREATED:
                    mock.create_recipe.return_value = Recipe(**expected_response)
                case status.HTTP_409_CONFLICT:
                    mock.create_recipe.side_effect = errors.RecipeExistsError(
                        name="Existing Recipe"
                    )
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_recipe_service] = (  # type: ignore
            mock_recipe_service
        )

        recipe_data = {
            "name": "Chocolate Cake",
            "prep_time_sec": 1800,
            "cook_time_sec": 2700,
            "servings": 8,
        }
        response = client.post("/recipes/", json=recipe_data)
        assert response.status_code == expected_status, response.text
        data = response.json()
        assert data == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, input_data, expected_status, expected_response", p.PUT_PARAMETERS
)
class TestPUT:
    def test_update_recipe(
        self,
        scenario: str,
        client_name: Role,
        input_data: dict,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test updating recipes with various scenarios."""

        def mock_recipe_service():
            mock = MagicMock()
            if scenario in ["update_full", "update_partial"]:
                mock.update_recipe.return_value = Recipe(**expected_response)
            elif scenario == "not_found":
                mock.update_recipe.side_effect = errors.RecipeNotFoundError(recipe_id=999)
            elif scenario == "conflict":
                mock.update_recipe.side_effect = errors.RecipeExistsError(name="Existing Recipe")
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_recipe_service] = mock_recipe_service  # type: ignore

        url = "/recipes/1" if scenario not in ["not_found"] else "/recipes/999"
        response = client.put(url, json=input_data)
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, recipe_id, expected_status, expected_response", p.DELETE_PARAMETERS
)
class TestDELETE:
    def test_delete_recipe(
        self,
        scenario: str,
        client_name: Role,
        recipe_id: int,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test deleting recipes with various scenarios."""

        def mock_recipe_service():
            mock = MagicMock()
            if scenario == "delete_success":
                mock.delete_recipe.return_value = None
            elif scenario == "delete_not_found":
                mock.delete_recipe.side_effect = errors.RecipeNotFoundError(recipe_id=recipe_id)
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_recipe_service] = mock_recipe_service  # type: ignore

        response = client.delete(f"/recipes/{recipe_id}")
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response
