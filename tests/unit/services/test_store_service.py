from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from docuisine.db.models import Store
from docuisine.services import StoreService
from docuisine.utils.errors import StoreExistsError, StoreNotFoundError


def test_create_store(db_session: MagicMock):
    """Test creating a new store."""
    service = StoreService(db_session)
    store: Store = service.create_store(
        name="Grocery Mart",
        address="123 Main St",
        longitude=-122.4194,
        latitude=37.7749,
        phone="555-1234",
        website="https://grocerymart.com",
        description="Local grocery store",
    )

    assert store.name == "Grocery Mart"
    assert store.address == "123 Main St"
    assert store.longitude == -122.4194
    assert store.latitude == 37.7749
    assert store.phone == "555-1234"
    assert store.website == "https://grocerymart.com"
    assert store.description == "Local grocery store"
    db_session.add.assert_called_once_with(store)
    db_session.commit.assert_called_once()


def test_create_store_minimal_fields(db_session: MagicMock):
    """Test creating a store with only required fields."""
    service = StoreService(db_session)
    store: Store = service.create_store(name="Corner Shop", address="456 Elm St")

    assert store.name == "Corner Shop"
    assert store.address == "456 Elm St"
    assert store.longitude is None
    assert store.latitude is None
    assert store.phone is None
    assert store.website is None
    assert store.description is None
    db_session.add.assert_called_once_with(store)
    db_session.commit.assert_called_once()


def test_create_store_duplicate_name_raises_error(db_session: MagicMock):
    """Test that creating a store with duplicate name raises StoreExistsError."""
    service = StoreService(db_session)
    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )

    with pytest.raises(StoreExistsError) as exc_info:
        service.create_store(name="Duplicate Store", address="789 Oak Ave")

    assert "Duplicate Store" in str(exc_info.value)
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.rollback.assert_called_once()


def test_get_store_by_id(db_session: MagicMock, monkeypatch):
    """Test retrieving a store by ID."""
    service = StoreService(db_session)
    example_store = Store(
        id=1, name="Supermarket", address="999 Broadway", description="Large supermarket"
    )
    monkeypatch.setattr(
        service,
        "_get_store_by_id",
        lambda store_id: example_store,
    )

    retrieved: Store = service.get_store(store_id=example_store.id)

    assert retrieved.name == "Supermarket"
    assert retrieved.address == "999 Broadway"


def test_get_store_by_name(db_session: MagicMock, monkeypatch):
    """Test retrieving a store by name."""
    service = StoreService(db_session)
    created = Store(id=1, name="Farmers Market", address="111 Park Ln")
    monkeypatch.setattr(
        service,
        "_get_store_by_name",
        lambda name: created,
    )

    retrieved: Store = service.get_store(name="Farmers Market")

    assert retrieved.id == created.id
    assert retrieved.name == "Farmers Market"


def test_get_store_not_found_by_id_raises_error(db_session: MagicMock, monkeypatch):
    """Test that getting a non-existent store by ID raises StoreNotFoundError."""
    service = StoreService(db_session)
    monkeypatch.setattr(service, "_get_store_by_id", lambda store_id: None)

    with pytest.raises(StoreNotFoundError) as exc_info:
        service.get_store(store_id=999)

    assert "999" in str(exc_info.value)


def test_get_store_not_found_by_name_raises_error(db_session: MagicMock, monkeypatch):
    """Test that getting a non-existent store by name raises StoreNotFoundError."""
    service = StoreService(db_session)
    monkeypatch.setattr(service, "_get_store_by_name", lambda name: None)

    with pytest.raises(StoreNotFoundError) as exc_info:
        service.get_store(name="NonExistent")

    assert "NonExistent" in str(exc_info.value)


def test_get_store_without_params_raises_error(db_session: MagicMock):
    """Test that calling get_store without parameters raises ValueError."""
    service = StoreService(db_session)

    with pytest.raises(ValueError) as exc_info:
        service.get_store()

    assert "Either store ID or name must be provided" in str(exc_info.value)


def test_get_all_stores(db_session: MagicMock):
    """Test retrieving all stores."""
    service = StoreService(db_session)
    store1 = Store(id=1, name="Store A", address="100 First St")
    store2 = Store(id=2, name="Store B", address="200 Second St")
    store3 = Store(id=3, name="Store C", address="300 Third St")
    db_session.query.return_value.all.return_value = [store1, store2, store3]

    all_stores = service.get_all_stores()

    assert len(all_stores) == 3
    store_names = {store.name for store in all_stores}
    assert store_names == {"Store A", "Store B", "Store C"}
    db_session.query.assert_called_once_with(Store)
    db_session.query.return_value.all.assert_called_once()


def test_update_store_name(db_session: MagicMock, monkeypatch):
    """Test updating a store's name."""
    service = StoreService(db_session)
    store: Store = Store(id=1, name="Old Name", address="555 Main St")
    monkeypatch.setattr(service, "_get_store_by_id", lambda x: store)

    updated: Store = service.update_store(store.id, name="New Name")

    db_session.commit.assert_called_once()
    assert updated.id == store.id
    assert updated.name == "New Name"
    assert updated.address == "555 Main St"


def test_update_store_address(db_session: MagicMock, monkeypatch):
    """Test updating a store's address."""
    service = StoreService(db_session)
    store: Store = Store(id=1, name="Shop", address="Old Address")
    monkeypatch.setattr(service, "_get_store_by_id", lambda x: store)

    updated: Store = service.update_store(store.id, address="New Address")

    db_session.commit.assert_called_once()
    assert updated.name == "Shop"
    assert updated.address == "New Address"


def test_update_store_coordinates(db_session: MagicMock, monkeypatch):
    """Test updating a store's coordinates."""
    service = StoreService(db_session)
    store: Store = Store(id=1, name="Store", address="123 St", longitude=None, latitude=None)
    monkeypatch.setattr(service, "_get_store_by_id", lambda x: store)

    updated: Store = service.update_store(store.id, longitude=-118.2437, latitude=34.0522)

    db_session.commit.assert_called_once()
    assert updated.longitude == -118.2437
    assert updated.latitude == 34.0522


def test_update_store_multiple_fields(db_session: MagicMock, monkeypatch):
    """Test updating multiple fields of a store."""
    service = StoreService(db_session)
    example: Store = Store(
        id=1,
        name="Old Store",
        address="Old Address",
        phone=None,
        website=None,
        description=None,
    )
    monkeypatch.setattr(service, "_get_store_by_id", lambda x: example)

    updated = service.update_store(
        example.id,
        name="Updated Store",
        address="Updated Address",
        phone="555-9999",
        website="https://updated.com",
        description="Updated description",
    )

    db_session.commit.assert_called_once()
    assert updated.id == example.id
    assert updated.name == "Updated Store"
    assert updated.address == "Updated Address"
    assert updated.phone == "555-9999"
    assert updated.website == "https://updated.com"
    assert updated.description == "Updated description"


def test_update_store_not_found_raises_error(db_session: MagicMock, monkeypatch):
    """Test that updating a non-existent store raises StoreNotFoundError."""
    service = StoreService(db_session)
    monkeypatch.setattr(service, "_get_store_by_id", lambda x: None)

    with pytest.raises(StoreNotFoundError) as exc_info:
        service.update_store(999, name="NewName")

    assert "999" in str(exc_info.value)


def test_update_store_duplicate_name_raises_error(db_session: MagicMock):
    """Test that updating to a duplicate name raises StoreExistsError."""
    service = StoreService(db_session)

    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )
    with pytest.raises(StoreExistsError) as exc_info:
        service.update_store(1, name="Existing Store")

    assert "Existing Store" in str(exc_info.value)
    db_session.commit.assert_called_once()
    db_session.rollback.assert_called_once()


def test_delete_store(db_session: MagicMock, monkeypatch):
    """Test deleting a store."""
    service = StoreService(db_session)
    example = Store(id=1, name="ToDelete", address="Delete St")
    monkeypatch.setattr(service, "_get_store_by_id", lambda id: example)

    service.delete_store(example.id)

    db_session.delete.assert_called_once_with(example)
    db_session.commit.assert_called_once()


def test_delete_store_not_found_raises_error(db_session: MagicMock, monkeypatch):
    """Test that deleting a non-existent store raises StoreNotFoundError."""
    service = StoreService(db_session)
    monkeypatch.setattr(service, "_get_store_by_id", lambda x: None)

    with pytest.raises(StoreNotFoundError) as exc_info:
        service.delete_store(999)

    assert "999" in str(exc_info.value)


def test_get_store_by_id_primitive(db_session: MagicMock):
    """
    Test retrieving a store by ID by testing correct
    calling procedure of primitive SQLAlchemy methods.
    """
    service = StoreService(db_session)
    example_store = Store(id=1, name="Test Store", address="Test Address")
    db_session.first.return_value = example_store

    result = service._get_store_by_id(store_id=1)

    assert result == example_store
    db_session.query.assert_called_once_with(Store)
    db_session.filter_by.assert_called_with(id=1)
    db_session.first.assert_called_once()


def test_get_store_by_name_primitive(db_session: MagicMock):
    """
    Test retrieving a store by name by testing correct
    calling procedure of primitive SQLAlchemy methods.
    """
    service = StoreService(db_session)
    example_store = Store(id=1, name="Test Store", address="Test Address")
    db_session.first.return_value = example_store

    result = service._get_store_by_name(name="Test Store")

    assert result == example_store
    db_session.query.assert_called_once_with(Store)
    db_session.filter_by.assert_called_with(name="Test Store")
    db_session.first.assert_called_once()
