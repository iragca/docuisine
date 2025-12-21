from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import Ingredient
from docuisine.dependencies import Ingredient_Service
from docuisine.schemas.common import Detail
from docuisine.schemas.ingredient import IngredientCreate, IngredientOut, IngredientUpdate
from docuisine.utils import errors

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[IngredientOut])
async def get_ingredients(ingredient_service: Ingredient_Service) -> list[IngredientOut]:
    """Get all ingredients."""
    ingredients: list[Ingredient] = ingredient_service.get_all_ingredients()
    return [IngredientOut.model_validate(ingredient) for ingredient in ingredients]


@router.get(
    "/{ingredient_id}",
    status_code=status.HTTP_200_OK,
    response_model=IngredientOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_ingredient(
    ingredient_id: int, ingredient_service: Ingredient_Service
) -> IngredientOut:
    """Get an ingredient by ID."""
    try:
        ingredient: Ingredient = ingredient_service.get_ingredient(ingredient_id=ingredient_id)
        return IngredientOut.model_validate(ingredient)
    except errors.IngredientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IngredientOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_ingredient(
    ingredient: IngredientCreate, ingredient_service: Ingredient_Service
) -> IngredientOut:
    """Create a new ingredient."""
    try:
        new_ingredient: Ingredient = ingredient_service.create_ingredient(
            name=ingredient.name,
            description=ingredient.description,
            recipe_id=ingredient.recipe_id,
        )
        return IngredientOut.model_validate(new_ingredient)
    except errors.IngredientExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.put(
    "/{ingredient_id}",
    status_code=status.HTTP_200_OK,
    response_model=IngredientOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_ingredient(
    ingredient_id: int, ingredient: IngredientUpdate, ingredient_service: Ingredient_Service
) -> IngredientOut:
    """Update an ingredient by ID."""
    try:
        updated_ingredient: Ingredient = ingredient_service.update_ingredient(
            ingredient_id=ingredient_id,
            name=ingredient.name,
            description=ingredient.description,
            recipe_id=ingredient.recipe_id,
        )
        return IngredientOut.model_validate(updated_ingredient)
    except errors.IngredientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except errors.IngredientExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_200_OK,
    response_model=Detail,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def delete_ingredient(ingredient_id: int, ingredient_service: Ingredient_Service) -> Detail:
    """Delete an ingredient by ID."""
    try:
        ingredient_service.delete_ingredient(ingredient_id=ingredient_id)
        return Detail(detail=f"Ingredient with ID {ingredient_id} has been deleted.")
    except errors.IngredientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
