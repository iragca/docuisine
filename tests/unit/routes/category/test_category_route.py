from typing import Callable
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import Category
from docuisine.dependencies.services import get_category_service, get_image_service
from docuisine.schemas.enums import Role
from docuisine.schemas.image import ImageSet
from docuisine.utils import errors

from . import params as p


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.GET_PARAMETERS
)
class TestGET:
    def test_get_categories(
        self,
        scenario: str,
        client_name: Role,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test getting categories."""

        def mock_category_service():
            mock = MagicMock()
            match scenario:
                case "get_all":
                    mock.get_all_categories.return_value = [
                        Category(**cat) for cat in p.GET_ALL_CATEGORIES_RESPONSE
                    ]
                case "get_by_id":
                    mock.get_category.return_value = Category(**p.GET_BY_ID_RESPONSE)
                case "get_not_found":
                    mock.get_category.side_effect = errors.CategoryNotFoundError(category_id=999)
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_category_service] = mock_category_service  # type: ignore

        match scenario:
            case "get_all":
                response = client.get("/categories/")
            case "get_by_id":
                response = client.get("/categories/1")
            case "get_not_found":
                response = client.get("/categories/999")
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.POST_PARAMETERS
)
class TestPOST:
    def test_create_category(
        self,
        scenario: str,
        client_name: Role,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test creating a category (success or conflict)."""

        ## Setup
        mock_category_service = MagicMock()
        mock_image_service = MagicMock()

        match scenario:
            case "success" | "success_no_description":
                mock_category_service.create_category.return_value = Category(**expected_response)
            case "conflict":
                mock_category_service.create_category.side_effect = errors.CategoryExistsError(
                    name="Dessert"
                )
            case "success_image_upload":
                mock_category_service.create_category.return_value = Category(**expected_response)
                mock_image_service.save_category_image.return_value = ImageSet(
                    original="appetizer_full.jpg",
                    preview="appetizer_preview.jpg",
                )
            case _:
                pass

        client = create_client(client_name)
        client.app.dependency_overrides[get_category_service] = lambda: mock_category_service  # type: ignore
        client.app.dependency_overrides[get_image_service] = lambda: mock_image_service  # type: ignore

        ## Test
        match scenario:
            case "success":
                response = client.post(
                    "/categories/",
                    data={"name": "Mexican", "description": "Mexican cuisine"},
                )
            case "success_no_description":
                response = client.post("/categories/", data={"name": "Vegan"})
            case "conflict":
                response = client.post(
                    "/categories/",
                    data={"name": "Dessert", "description": "Sweet dishes"},
                )
            case "unauthorized":
                response = client.post(
                    "/categories/",
                    data={"name": "Unauthorized", "description": "Should not work"},
                )
                assert mock_category_service.create_category.call_count == 0
            case "success_image_upload":
                response = client.post(
                    "/categories/",
                    data={"name": "Appetizer", "description": "Starters"},
                    files={"image": ("test_image.jpg", b"image-bytes", "image/jpeg")},
                )
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.PUT_PARAMETERS
)
class TestPUT:
    def test_update_category(
        self,
        scenario: str,
        client_name: Role,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test updating a category successfully."""

        mock_category_service = MagicMock()
        match scenario:
            case "update_not_found":
                mock_category_service.update_category.side_effect = errors.CategoryNotFoundError(
                    category_id=1
                )
            case "update_conflict":
                mock_category_service.update_category.side_effect = errors.CategoryExistsError(
                    name="Dessert"
                )
            case "update_name_only":
                mock_category_service.update_category.return_value = Category(
                    id=1, name="Updated Name", description="Original description"
                )
            case _:
                mock_category_service.update_category.return_value = Category(
                    id=1,
                    name="Desserts",
                    description="Updated description",
                    img="test",
                    preview_img="test",
                )

        client = create_client(client_name)
        client.app.dependency_overrides[get_category_service] = lambda: mock_category_service  # type: ignore
        match scenario:
            case "update_name_only":
                update_data = {"id": 1, "name": "Desserts"}
            case _:
                update_data = {
                    "id": 1,
                    "name": "Desserts",
                    "description": "Updated description",
                    "img": "test",
                    "preview_img": "test",
                }
        response = client.put("/categories", json=update_data)
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


class TestDELETE:
    @pytest.mark.parametrize(
        "scenario, client_name, category_id, expected_status, expected_response",
        p.DELETE_PARAMETERS,
    )
    def test_delete_category(
        self,
        scenario: str,
        client_name: Role,
        category_id: int,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test deleting a category successfully."""

        mock_category_service = MagicMock()
        match scenario:
            case "delete_not_found":
                mock_category_service.delete_category.side_effect = errors.CategoryNotFoundError(
                    category_id=category_id
                )
            case _:
                mock_category_service.delete_category.return_value = None

        client = create_client(client_name)
        client.app.dependency_overrides[get_category_service] = lambda: mock_category_service  # type: ignore

        response = client.delete(f"/categories/{category_id}")
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response
