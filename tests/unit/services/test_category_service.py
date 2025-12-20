from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from docuisine.db.models import Category
from docuisine.services import CategoryService
from docuisine.utils.errors import CategoryExistsError, CategoryNotFoundError


def test_create_category(db_session: MagicMock):
    """Test creating a new category."""
    service = CategoryService(db_session)
    category: Category = service.create_category(name="Dessert", description="Sweet treats")

    assert category.name == "Dessert"
    assert category.description == "Sweet treats"


def test_create_category_without_description(db_session: MagicMock):
    """Test creating a category without a description."""
    service = CategoryService(db_session)
    category: Category = service.create_category(name="Vegetarian")

    assert category.name == "Vegetarian"
    assert category.description is None


def test_create_category_duplicate_name_raises_error(db_session: MagicMock):
    """Test that creating a category with duplicate name raises CategoryExistsError."""
    service = CategoryService(db_session)
    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )

    with pytest.raises(CategoryExistsError) as exc_info:
        service.create_category(name="Dessert")

    assert "Dessert" in str(exc_info.value)


def test_get_category_by_id(db_session: MagicMock, monkeypatch):
    """Test retrieving a category by ID."""
    service = CategoryService(db_session)
    example_category = Category(id=1, name="Korean", description="Korean cuisine")
    monkeypatch.setattr(
        service,
        "_get_category_by_id",
        lambda category_id: example_category,
    )

    retrieved_category: Category = service.get_category(category_id=example_category.id)

    # assert retrieved_category.id == example_category.id
    assert retrieved_category.name == "Korean"
    # assert retrieved_category.description == "Korean cuisine"


def test_get_category_by_name(db_session: MagicMock, monkeypatch):
    """Test retrieving a category by name."""
    service = CategoryService(db_session)
    created_category = Category(id=1, name="Italian")
    monkeypatch.setattr(
        service,
        "_get_category_by_name",
        lambda name: created_category,
    )

    retrieved_category: Category = service.get_category(name="Italian")

    assert retrieved_category.id == created_category.id
    assert retrieved_category.name == "Italian"


def test_get_category_not_found_by_id_raises_error(db_session: MagicMock, monkeypatch):
    """Test that getting a non-existent category by ID raises CategoryNotFoundError."""
    service = CategoryService(db_session)
    monkeypatch.setattr(
        service,
        "_get_category_by_id",
        lambda category_id: None,
    )

    with pytest.raises(CategoryNotFoundError) as exc_info:
        service.get_category(category_id=999)

    assert "999" in str(exc_info.value)


def test_get_category_not_found_by_name_raises_error(db_session: MagicMock, monkeypatch):
    """Test that getting a non-existent category by name raises CategoryNotFoundError."""
    service = CategoryService(db_session)
    monkeypatch.setattr(
        service,
        "_get_category_by_name",
        lambda name: None,
    )

    with pytest.raises(CategoryNotFoundError) as exc_info:
        service.get_category(name="NonExistent")

    assert "NonExistent" in str(exc_info.value)


def test_get_category_without_params_raises_error(db_session: MagicMock):
    """Test that calling get_category without parameters raises ValueError."""
    service = CategoryService(db_session)

    with pytest.raises(ValueError) as exc_info:
        service.get_category()

    assert "Either category ID or name must be provided" in str(exc_info.value)


def test_get_all_categories(db_session: MagicMock):
    """Test retrieving all categories."""
    service = CategoryService(db_session)
    cat1 = Category(id=1, name="Mexican")
    cat2 = Category(id=2, name="Japanese")
    cat3 = Category(id=3, name="Indian")
    db_session.query.return_value.all.return_value = [cat1, cat2, cat3]

    all_categories = service.get_all_categories()

    assert len(all_categories) == 3
    category_names = {cat.name for cat in all_categories}
    assert category_names == {"Mexican", "Japanese", "Indian"}


def test_update_category_name(db_session: MagicMock, monkeypatch):
    """Test updating a category's name."""
    service = CategoryService(db_session)
    category: Category = Category(id=1, name="Deserts", description="Sweet dishes")
    monkeypatch.setattr(
        service,
        "_get_category_by_id",
        lambda x: category,
    )

    updated_category: Category = service.update_category(category.id, name="Desserts")

    db_session.commit.assert_called_once()
    assert updated_category.id == category.id
    assert updated_category.name == "Desserts"
    assert updated_category.description == category.description


def test_update_category_description(db_session: MagicMock, monkeypatch):
    """Test updating a category's description."""
    service = CategoryService(db_session)
    category: Category = Category(id=1, name="Vegan", description="No animal products")
    monkeypatch.setattr(
        service,
        "_get_category_by_id",
        lambda x: category,
    )

    updated_category: Category = service.update_category(
        category.id, description="Plant-based dishes"
    )

    db_session.commit.assert_called_once()
    assert updated_category.id == category.id
    assert updated_category.name == "Vegan"
    assert updated_category.description == "Plant-based dishes"


def test_update_category_both_fields(db_session: MagicMock, monkeypatch):
    """Test updating both name and description of a category."""
    service = CategoryService(db_session)
    example_category: Category = Category(id=1, name="QuickMeals", description="Fast recipes")
    monkeypatch.setattr(
        service,
        "_get_category_by_id",
        lambda x: example_category,
    )

    updated_category = service.update_category(
        example_category.id, name="Quick & Easy", description="Fast and simple meals"
    )
    db_session.commit.assert_called_once()
    assert updated_category.id == example_category.id
    assert updated_category.name == "Quick & Easy"
    assert updated_category.description == "Fast and simple meals"


def test_update_category_not_found_raises_error(db_session: MagicMock, monkeypatch):
    """Test that updating a non-existent category raises CategoryNotFoundError."""
    service = CategoryService(db_session)
    monkeypatch.setattr(service, "_get_category_by_id", lambda x: None)

    with pytest.raises(CategoryNotFoundError) as exc_info:
        service.update_category(999, name="NewName")

    assert "999" in str(exc_info.value)


def test_update_category_duplicate_name_raises_error(db_session: MagicMock):
    """Test that updating to a duplicate name raises CategoryExistsError."""
    service = CategoryService(db_session)

    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )
    with pytest.raises(CategoryExistsError) as exc_info:
        service.update_category(1, name="Breakfast")

    assert "Breakfast" in str(exc_info.value)


def test_delete_category(db_session: MagicMock, monkeypatch):
    """Test deleting a category."""
    service = CategoryService(db_session)
    example_category = Category(id=1, name="ToDelete", description="To be deleted")
    monkeypatch.setattr(
        service,
        "_get_category_by_id",
        lambda id: example_category,
    )
    service.delete_category(example_category.id)
    db_session.delete.assert_called_once_with(example_category)
    db_session.commit.assert_called_once()


def test_delete_category_not_found_raises_error(db_session: MagicMock, monkeypatch):
    """Test that deleting a non-existent category raises CategoryNotFoundError."""
    service = CategoryService(db_session)
    monkeypatch.setattr(service, "_get_category_by_id", lambda x: None)

    with pytest.raises(CategoryNotFoundError) as exc_info:
        service.delete_category(999)

    assert "999" in str(exc_info.value)
