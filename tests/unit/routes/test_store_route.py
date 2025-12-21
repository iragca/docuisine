from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient

from docuisine.db.models import Store
from docuisine.dependencies.services import get_store_service
from docuisine.main import app
from docuisine.utils import errors


def test_get_stores():
    """Test getting all stores."""

    def mock_store_service():
        mock = MagicMock()
        mock_stores = [
            Store(id=1, name="Grocery Mart", address="123 Main St"),
            Store(id=2, name="Corner Shop", address="456 Elm St"),
            Store(id=3, name="Organic Market", address="789 Oak Ave", description=None),
        ]
        mock.get_all_stores.return_value = mock_stores
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    response = client.get("/stores/")
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Grocery Mart"
    assert data[0]["address"] == "123 Main St"
    assert data[1]["name"] == "Corner Shop"
    assert data[2]["name"] == "Organic Market"
    assert "id" in data[0] and "id" in data[1]


def test_get_store_by_id():
    """Test getting a store by ID."""

    def mock_store_service():
        mock = MagicMock()
        mock.get_store.return_value = Store(
            id=1,
            name="Supermarket",
            address="999 Broadway",
            longitude=-118.2437,
            latitude=34.0522,
            phone="555-0000",
            website="https://supermarket.com",
            description="Large supermarket",
        )
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    response = client.get("/stores/1")
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Supermarket"
    assert data["address"] == "999 Broadway"
    assert data["longitude"] == -118.2437
    assert data["latitude"] == 34.0522
    assert data["phone"] == "555-0000"
    assert data["website"] == "https://supermarket.com"
    assert data["description"] == "Large supermarket"


def test_get_store_not_found():
    """Test getting a non-existent store returns 404."""

    def mock_store_service():
        mock = MagicMock()
        mock.get_store.side_effect = errors.StoreNotFoundError(store_id=999)
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    response = client.get("/stores/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == "Store with ID 999 not found."


def test_create_store_success():
    """Test creating a new store successfully."""

    def mock_store_service():
        mock = MagicMock()
        mock.create_store.return_value = Store(
            id=1,
            name="New Store",
            address="111 First St",
            description="Nice store",
        )
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    store_data = {
        "name": "New Store",
        "address": "111 First St",
        "description": "Nice store",
    }
    response = client.post("/stores/", json=store_data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "New Store"
    assert data["address"] == "111 First St"
    assert data["description"] == "Nice store"
    assert data["id"] == 1


def test_create_store_minimal_fields():
    """Test creating a store with only required fields."""

    def mock_store_service():
        mock = MagicMock()
        mock.create_store.return_value = Store(id=2, name="Mini", address="222 Second St")
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    store_data = {"name": "Mini", "address": "222 Second St"}
    response = client.post("/stores/", json=store_data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "Mini"
    assert data["address"] == "222 Second St"


def test_create_store_conflict():
    """Test creating a store with duplicate name returns 409."""

    def mock_store_service():
        mock = MagicMock()
        mock.create_store.side_effect = errors.StoreExistsError(name="Existing Store")
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    store_data = {"name": "Existing Store", "address": "333 Third St"}
    response = client.post("/stores/", json=store_data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "Store with name 'Existing Store' already exists."


def test_update_store_success():
    """Test updating a store successfully."""

    def mock_store_service():
        mock = MagicMock()
        mock.update_store.return_value = Store(
            id=1,
            name="Updated Store",
            address="Updated Address",
            phone="555-9999",
            website="https://updated.com",
            description="Updated description",
        )
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    update_data = {
        "name": "Updated Store",
        "address": "Updated Address",
        "phone": "555-9999",
        "website": "https://updated.com",
        "description": "Updated description",
    }
    response = client.put("/stores/1", json=update_data)
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Updated Store"
    assert data["address"] == "Updated Address"
    assert data["phone"] == "555-9999"
    assert data["website"] == "https://updated.com"
    assert data["description"] == "Updated description"


def test_update_store_partial():
    """Test updating only some fields."""

    def mock_store_service():
        mock = MagicMock()
        mock.update_store.return_value = Store(
            id=1,
            name="Shop",
            address="New Address",
        )
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    update_data = {"address": "New Address"}
    response = client.put("/stores/1", json=update_data)
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["address"] == "New Address"


def test_update_store_not_found():
    """Test updating a non-existent store returns 404."""

    def mock_store_service():
        mock = MagicMock()
        mock.update_store.side_effect = errors.StoreNotFoundError(store_id=999)
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    update_data = {"name": "New Name"}
    response = client.put("/stores/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == "Store with ID 999 not found."


def test_update_store_conflict():
    """Test updating to a duplicate name returns 409."""

    def mock_store_service():
        mock = MagicMock()
        mock.update_store.side_effect = errors.StoreExistsError(name="Existing Store")
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    update_data = {"name": "Existing Store"}
    response = client.put("/stores/1", json=update_data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "Store with name 'Existing Store' already exists."


def test_delete_store_success():
    """Test deleting a store successfully."""

    def mock_store_service():
        mock = MagicMock()
        mock.delete_store.return_value = None
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    response = client.delete("/stores/1")
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["detail"] == "Store with ID 1 has been deleted."


def test_delete_store_not_found():
    """Test deleting a non-existent store returns 404."""

    def mock_store_service():
        mock = MagicMock()
        mock.delete_store.side_effect = errors.StoreNotFoundError(store_id=999)
        return mock

    app.dependency_overrides[get_store_service] = mock_store_service
    client = TestClient(app)

    response = client.delete("/stores/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == "Store with ID 999 not found."
