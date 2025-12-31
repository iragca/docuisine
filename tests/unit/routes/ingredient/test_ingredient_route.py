from typing import Callable
from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import Ingredient
from docuisine.dependencies.services import get_ingredient_service
from docuisine.schemas import Role
from docuisine.utils import errors

from . import params as p


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.GET_PARAMETERS
)
class TestGET:
    def test_get_ingredient(
        self,
        scenario: str,
        client_name: Role,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test GET routes for all scenarios (all ingredients, by ID, not found)."""

        def mock_ingredient_service():
            mock = MagicMock()
            if scenario == "get_all":
                mock.get_all_ingredients.return_value = [
                    Ingredient(**ing) for ing in p.GET_INGREDIENTS_RESPONSE
                ]
            elif scenario == "get_by_id":
                mock.get_ingredient.return_value = Ingredient(**p.GET_INGREDIENT_BY_ID_RESPONSE)
            elif scenario == "get_not_found":
                mock.get_ingredient.side_effect = errors.IngredientNotFoundError(ingredient_id=999)
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_ingredient_service] = mock_ingredient_service  # type: ignore

        # Make the request
        if scenario == "get_all":
            response = client.get("/ingredients")
        elif scenario in ["get_by_id", "get_not_found"]:
            response = client.get(
                "/ingredients/1" if scenario == "get_by_id" else "/ingredients/999"
            )

        # Assertions
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


class TestPOST:
    @pytest.mark.parametrize(
        "client_name, expected_status, post_response",
        p.POST_PARAMETERS,
    )
    def test_create_ingredient(
        self,
        client_name: Role,
        expected_status: int,
        post_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test creating a new ingredient."""

        ## Setup
        def mock_ingredient_service():
            mock = MagicMock()
            match expected_status:
                case status.HTTP_201_CREATED:
                    mock.create_ingredient.return_value = Ingredient(**post_response)
                case status.HTTP_409_CONFLICT:
                    mock.create_ingredient.side_effect = errors.IngredientExistsError(name="Eggs")
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_ingredient_service] = (  # type: ignore
            mock_ingredient_service
        )

        ## Test
        ingredient_data = {"name": "Eggs", "description": "Large eggs"}
        response = client.post("/ingredients", json=ingredient_data)
        assert response.status_code == expected_status, response.text
        data = response.json()
        assert data == post_response


@pytest.mark.parametrize(
    "scenario, client_name, input_data, expected_status, expected_response", p.PUT_PARAMETERS
)
class TestPUT:
    def test_update_ingredient(
        self,
        scenario: str,
        client_name: Role,
        input_data: dict,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test updating ingredients with various scenarios."""

        def mock_ingredient_service():
            mock = MagicMock()
            if scenario in ["update_full", "update_partial", "update_recipe_id"]:
                mock.update_ingredient.return_value = Ingredient(**expected_response)
            elif scenario == "not_found":
                mock.update_ingredient.side_effect = errors.IngredientNotFoundError(
                    ingredient_id=999
                )
            elif scenario == "conflict":
                mock.update_ingredient.side_effect = errors.IngredientExistsError(name="Existing")
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_ingredient_service] = mock_ingredient_service  # type: ignore

        url = "/ingredients/1" if scenario not in ["not_found", "conflict"] else "/ingredients/999"
        response = client.put(url, json=input_data)
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, ingredient_id, expected_status, expected_response", p.DELETE_PARAMETERS
)
class TestDELETE:
    def test_delete_ingredient(
        self,
        scenario: str,
        client_name: Role,
        ingredient_id: int,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test deleting ingredients with various scenarios."""

        def mock_ingredient_service():
            mock = MagicMock()
            if scenario == "delete_success":
                mock.delete_ingredient.return_value = None
            elif scenario == "delete_not_found":
                mock.delete_ingredient.side_effect = errors.IngredientNotFoundError(
                    ingredient_id=ingredient_id
                )
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_ingredient_service] = mock_ingredient_service  # type: ignore

        response = client.delete(f"/ingredients/{ingredient_id}")
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response
