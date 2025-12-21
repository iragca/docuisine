from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from docuisine.db.models import Recipe
from docuisine.services import RecipeService
from docuisine.utils.errors import RecipeExistsError, RecipeNotFoundError


def test_create_recipe(db_session: MagicMock):
    """Test creating a new recipe."""
    service = RecipeService(db_session)
    recipe: Recipe = service.create_recipe(
        user_id=1,
        name="Chocolate Cake",
        cook_time_sec=3600,
        prep_time_sec=1200,
        non_blocking_time_sec=600,
        servings=8,
        description="Delicious chocolate cake",
    )

    assert recipe.user_id == 1
    assert recipe.name == "Chocolate Cake"
    assert recipe.cook_time_sec == 3600
    assert recipe.prep_time_sec == 1200
    assert recipe.non_blocking_time_sec == 600
    assert recipe.servings == 8
    assert recipe.description == "Delicious chocolate cake"
    db_session.add.assert_called_once_with(recipe)
    db_session.commit.assert_called_once()


def test_create_recipe_minimal_fields(db_session: MagicMock):
    """Test creating a recipe with only required fields."""
    service = RecipeService(db_session)
    recipe: Recipe = service.create_recipe(user_id=1, name="Simple Recipe")

    assert recipe.user_id == 1
    assert recipe.name == "Simple Recipe"
    assert recipe.cook_time_sec is None
    assert recipe.prep_time_sec is None
    assert recipe.non_blocking_time_sec is None
    assert recipe.servings is None
    assert recipe.description is None
    db_session.add.assert_called_once_with(recipe)
    db_session.commit.assert_called_once()


def test_create_recipe_duplicate_name_raises_error(db_session: MagicMock):
    """Test that creating a recipe with duplicate name raises RecipeExistsError."""
    service = RecipeService(db_session)
    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )

    with pytest.raises(RecipeExistsError) as exc_info:
        service.create_recipe(user_id=1, name="Duplicate Recipe")

    assert "Duplicate Recipe" in str(exc_info.value)
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.rollback.assert_called_once()


def test_get_recipe_by_id(db_session: MagicMock, monkeypatch):
    """Test retrieving a recipe by ID."""
    service = RecipeService(db_session)
    example_recipe = Recipe(
        id=1, user_id=1, name="Pasta Carbonara", description="Classic Italian pasta"
    )
    monkeypatch.setattr(
        service,
        "_get_recipe_by_id",
        lambda recipe_id: example_recipe,
    )

    retrieved: Recipe = service.get_recipe(recipe_id=example_recipe.id)

    assert retrieved.name == "Pasta Carbonara"
    assert retrieved.description == "Classic Italian pasta"


def test_get_recipe_by_name(db_session: MagicMock, monkeypatch):
    """Test retrieving a recipe by name."""
    service = RecipeService(db_session)
    created = Recipe(id=1, user_id=1, name="Pizza Margherita")
    monkeypatch.setattr(
        service,
        "_get_recipe_by_name",
        lambda name: created,
    )

    retrieved: Recipe = service.get_recipe(name="Pizza Margherita")

    assert retrieved.id == created.id
    assert retrieved.name == "Pizza Margherita"


def test_get_recipe_not_found_by_id_raises_error(db_session: MagicMock, monkeypatch):
    """Test that getting a non-existent recipe by ID raises RecipeNotFoundError."""
    service = RecipeService(db_session)
    monkeypatch.setattr(service, "_get_recipe_by_id", lambda recipe_id: None)

    with pytest.raises(RecipeNotFoundError) as exc_info:
        service.get_recipe(recipe_id=999)

    assert "999" in str(exc_info.value)


def test_get_recipe_not_found_by_name_raises_error(db_session: MagicMock, monkeypatch):
    """Test that getting a non-existent recipe by name raises RecipeNotFoundError."""
    service = RecipeService(db_session)
    monkeypatch.setattr(service, "_get_recipe_by_name", lambda name: None)

    with pytest.raises(RecipeNotFoundError) as exc_info:
        service.get_recipe(name="NonExistent")

    assert "NonExistent" in str(exc_info.value)


def test_get_recipe_without_params_raises_error(db_session: MagicMock):
    """Test that calling get_recipe without parameters raises ValueError."""
    service = RecipeService(db_session)

    with pytest.raises(ValueError) as exc_info:
        service.get_recipe()

    assert "Either recipe ID or name must be provided" in str(exc_info.value)


def test_get_all_recipes(db_session: MagicMock):
    """Test retrieving all recipes."""
    service = RecipeService(db_session)
    recipe1 = Recipe(id=1, user_id=1, name="Recipe A")
    recipe2 = Recipe(id=2, user_id=1, name="Recipe B")
    recipe3 = Recipe(id=3, user_id=2, name="Recipe C")
    db_session.query.return_value.all.return_value = [recipe1, recipe2, recipe3]

    all_recipes = service.get_all_recipes()

    assert len(all_recipes) == 3
    recipe_names = {recipe.name for recipe in all_recipes}
    assert recipe_names == {"Recipe A", "Recipe B", "Recipe C"}
    db_session.query.assert_called_once_with(Recipe)
    db_session.query.return_value.all.assert_called_once()


def test_get_recipes_by_user(db_session: MagicMock):
    """Test retrieving recipes by user ID."""
    service = RecipeService(db_session)
    recipe1 = Recipe(id=1, user_id=5, name="User5 Recipe A")
    recipe2 = Recipe(id=2, user_id=5, name="User5 Recipe B")
    db_session.query.return_value.filter_by.return_value.all.return_value = [recipe1, recipe2]

    user_recipes = service.get_recipes_by_user(user_id=5)

    assert len(user_recipes) == 2
    assert all(recipe.user_id == 5 for recipe in user_recipes)
    db_session.query.assert_called_once_with(Recipe)
    db_session.query.return_value.filter_by.assert_called_once_with(user_id=5)


def test_update_recipe_name(db_session: MagicMock, monkeypatch):
    """Test updating a recipe's name."""
    service = RecipeService(db_session)
    recipe: Recipe = Recipe(id=1, user_id=1, name="Old Name", description="Some description")
    monkeypatch.setattr(service, "_get_recipe_by_id", lambda x: recipe)

    updated: Recipe = service.update_recipe(recipe.id, name="New Name")

    db_session.commit.assert_called_once()
    assert updated.id == recipe.id
    assert updated.name == "New Name"
    assert updated.description == "Some description"


def test_update_recipe_times(db_session: MagicMock, monkeypatch):
    """Test updating a recipe's time fields."""
    service = RecipeService(db_session)
    recipe: Recipe = Recipe(
        id=1,
        user_id=1,
        name="Recipe",
        cook_time_sec=None,
        prep_time_sec=None,
        non_blocking_time_sec=None,
    )
    monkeypatch.setattr(service, "_get_recipe_by_id", lambda x: recipe)

    updated: Recipe = service.update_recipe(
        recipe.id, cook_time_sec=1800, prep_time_sec=600, non_blocking_time_sec=300
    )

    db_session.commit.assert_called_once()
    assert updated.cook_time_sec == 1800
    assert updated.prep_time_sec == 600
    assert updated.non_blocking_time_sec == 300


def test_update_recipe_servings_and_description(db_session: MagicMock, monkeypatch):
    """Test updating a recipe's servings and description."""
    service = RecipeService(db_session)
    recipe: Recipe = Recipe(id=1, user_id=1, name="Recipe", servings=None, description=None)
    monkeypatch.setattr(service, "_get_recipe_by_id", lambda x: recipe)

    updated: Recipe = service.update_recipe(
        recipe.id, servings=4, description="Updated description"
    )

    db_session.commit.assert_called_once()
    assert updated.servings == 4
    assert updated.description == "Updated description"


def test_update_recipe_multiple_fields(db_session: MagicMock, monkeypatch):
    """Test updating multiple fields of a recipe."""
    service = RecipeService(db_session)
    example: Recipe = Recipe(
        id=1,
        user_id=1,
        name="Old Recipe",
        cook_time_sec=None,
        prep_time_sec=None,
        servings=None,
        description=None,
    )
    monkeypatch.setattr(service, "_get_recipe_by_id", lambda x: example)

    updated = service.update_recipe(
        example.id,
        name="Updated Recipe",
        cook_time_sec=2400,
        prep_time_sec=900,
        servings=6,
        description="Fully updated",
    )

    db_session.commit.assert_called_once()
    assert updated.id == example.id
    assert updated.name == "Updated Recipe"
    assert updated.cook_time_sec == 2400
    assert updated.prep_time_sec == 900
    assert updated.servings == 6
    assert updated.description == "Fully updated"


def test_update_recipe_not_found_raises_error(db_session: MagicMock, monkeypatch):
    """Test that updating a non-existent recipe raises RecipeNotFoundError."""
    service = RecipeService(db_session)
    monkeypatch.setattr(service, "_get_recipe_by_id", lambda x: None)

    with pytest.raises(RecipeNotFoundError) as exc_info:
        service.update_recipe(999, name="NewName")

    assert "999" in str(exc_info.value)


def test_update_recipe_duplicate_name_raises_error(db_session: MagicMock):
    """Test that updating to a duplicate name raises RecipeExistsError."""
    service = RecipeService(db_session)

    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )
    with pytest.raises(RecipeExistsError) as exc_info:
        service.update_recipe(1, name="Existing Recipe")

    assert "Existing Recipe" in str(exc_info.value)
    db_session.commit.assert_called_once()
    db_session.rollback.assert_called_once()


def test_delete_recipe(db_session: MagicMock, monkeypatch):
    """Test deleting a recipe."""
    service = RecipeService(db_session)
    example = Recipe(id=1, user_id=1, name="ToDelete")
    monkeypatch.setattr(service, "_get_recipe_by_id", lambda id: example)

    service.delete_recipe(example.id)

    db_session.delete.assert_called_once_with(example)
    db_session.commit.assert_called_once()


def test_delete_recipe_not_found_raises_error(db_session: MagicMock, monkeypatch):
    """Test that deleting a non-existent recipe raises RecipeNotFoundError."""
    service = RecipeService(db_session)
    monkeypatch.setattr(service, "_get_recipe_by_id", lambda x: None)

    with pytest.raises(RecipeNotFoundError) as exc_info:
        service.delete_recipe(999)

    assert "999" in str(exc_info.value)


def test_get_recipe_by_id_primitive(db_session: MagicMock):
    """
    Test retrieving a recipe by ID by testing correct
    calling procedure of primitive SQLAlchemy methods.
    """
    service = RecipeService(db_session)
    example_recipe = Recipe(id=1, user_id=1, name="Test Recipe")
    db_session.first.return_value = example_recipe

    result = service._get_recipe_by_id(recipe_id=1)

    assert result == example_recipe
    db_session.query.assert_called_once_with(Recipe)
    db_session.filter_by.assert_called_with(id=1)
    db_session.first.assert_called_once()


def test_get_recipe_by_name_primitive(db_session: MagicMock):
    """
    Test retrieving a recipe by name by testing correct
    calling procedure of primitive SQLAlchemy methods.
    """
    service = RecipeService(db_session)
    example_recipe = Recipe(id=1, user_id=1, name="Test Recipe")
    db_session.first.return_value = example_recipe

    result = service._get_recipe_by_name(name="Test Recipe")

    assert result == example_recipe
    db_session.query.assert_called_once_with(Recipe)
    db_session.filter_by.assert_called_with(name="Test Recipe")
    db_session.first.assert_called_once()
