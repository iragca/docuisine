from typing import Callable
from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import Store
from docuisine.dependencies.services import get_store_service
from docuisine.schemas import Role
from docuisine.utils import errors

from . import params as p


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.GET_PARAMETERS
)
class TestGET:
    def test_get_store(
        self,
        scenario: str,
        client_name: Role,
        expected_status: int,
        expected_response: dict | list,
        create_client: Callable[[Role], TestClient],
    ):
        """Test GET routes for all scenarios (all stores, by ID, not found)."""

        def mock_store_service():
            mock = MagicMock()
            if scenario == "get_all":
                mock.get_all_stores.return_value = [
                    Store(**store) for store in p.GET_ALL_STORES_RESPONSE
                ]
            elif scenario == "get_by_id":
                mock.get_store.return_value = Store(**p.GET_STORE_BY_ID_RESPONSE)
            elif scenario == "get_not_found":
                mock.get_store.side_effect = errors.StoreNotFoundError(store_id=999)
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_store_service] = mock_store_service  # type: ignore

        # Make the request
        if scenario == "get_all":
            response = client.get("/stores/")
        elif scenario in ["get_by_id", "get_not_found"]:
            response = client.get("/stores/1" if scenario == "get_by_id" else "/stores/999")

        # Assertions
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


class TestPOST:
    @pytest.mark.parametrize(
        "client_name, expected_status, expected_response",
        p.POST_PARAMETERS,
    )
    def test_create_store(
        self,
        client_name: Role,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test creating a new store."""

        def mock_store_service():
            mock = MagicMock()
            match expected_status:
                case status.HTTP_201_CREATED:
                    mock.create_store.return_value = Store(**expected_response)
                case status.HTTP_409_CONFLICT:
                    mock.create_store.side_effect = errors.StoreExistsError(name="Existing Store")
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_store_service] = (  # type: ignore
            mock_store_service
        )

        store_data = {
            "name": "New Store",
            "address": "111 First St",
            "description": "Nice store",
        }
        response = client.post("/stores/", json=store_data)
        assert response.status_code == expected_status, response.text
        data = response.json()
        assert data == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, input_data, expected_status, expected_response", p.PUT_PARAMETERS
)
class TestPUT:
    def test_update_store(
        self,
        scenario: str,
        client_name: Role,
        input_data: dict,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test updating stores with various scenarios."""

        def mock_store_service():
            mock = MagicMock()
            if scenario in ["update_full", "update_partial"]:
                mock.update_store.return_value = Store(**expected_response)
            elif scenario == "not_found":
                mock.update_store.side_effect = errors.StoreNotFoundError(store_id=999)
            elif scenario == "conflict":
                mock.update_store.side_effect = errors.StoreExistsError(name="Existing Store")
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_store_service] = mock_store_service  # type: ignore

        url = "/stores/1" if scenario not in ["not_found"] else "/stores/999"
        response = client.put(url, json=input_data)
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, store_id, expected_status, expected_response", p.DELETE_PARAMETERS
)
class TestDELETE:
    def test_delete_store(
        self,
        scenario: str,
        client_name: Role,
        store_id: int,
        expected_status: int,
        expected_response: dict,
        create_client: Callable[[Role], TestClient],
    ):
        """Test deleting stores with various scenarios."""

        def mock_store_service():
            mock = MagicMock()
            if scenario == "delete_success":
                mock.delete_store.return_value = None
            elif scenario == "delete_not_found":
                mock.delete_store.side_effect = errors.StoreNotFoundError(store_id=store_id)
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_store_service] = mock_store_service  # type: ignore

        response = client.delete(f"/stores/{store_id}")
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response
