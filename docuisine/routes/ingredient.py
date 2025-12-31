from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import Ingredient
from docuisine.dependencies import AuthenticatedUser, Ingredient_Service
from docuisine.schemas import ingredient as ingredient_schemas
from docuisine.schemas.common import Detail
from docuisine.utils import errors
from docuisine.utils.validation import validate_role

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[ingredient_schemas.IngredientOut]
)
async def get_ingredients(
    ingredient_service: Ingredient_Service,
) -> list[ingredient_schemas.IngredientOut]:
    """
    Get all ingredients.

    Access Level: Public
    """
    ingredients: list[Ingredient] = ingredient_service.get_all_ingredients()
    return [
        ingredient_schemas.IngredientOut.model_validate(ingredient) for ingredient in ingredients
    ]


@router.get(
    "/{ingredient_id}",
    status_code=status.HTTP_200_OK,
    response_model=ingredient_schemas.IngredientOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_ingredient(
    ingredient_id: int, ingredient_service: Ingredient_Service
) -> ingredient_schemas.IngredientOut:
    """
    Get an ingredient by ID.

    Access Level: Public
    """
    try:
        ingredient: Ingredient = ingredient_service.get_ingredient(ingredient_id=ingredient_id)
        return ingredient_schemas.IngredientOut.model_validate(ingredient)
    except errors.IngredientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ingredient_schemas.IngredientOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_ingredient(
    ingredient: ingredient_schemas.IngredientCreate,
    ingredient_service: Ingredient_Service,
    authenticated_user: AuthenticatedUser,
) -> ingredient_schemas.IngredientOut:
    """
    Create a new ingredient.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
    try:
        new_ingredient: Ingredient = ingredient_service.create_ingredient(
            name=ingredient.name,
            description=ingredient.description,
            recipe_id=ingredient.recipe_id,
        )
        return ingredient_schemas.IngredientOut.model_validate(new_ingredient)
    except errors.IngredientExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.put(
    "/{ingredient_id}",
    status_code=status.HTTP_200_OK,
    response_model=ingredient_schemas.IngredientOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_ingredient(
    ingredient_id: int,
    ingredient: ingredient_schemas.IngredientUpdate,
    ingredient_service: Ingredient_Service,
    authenticated_user: AuthenticatedUser,
) -> ingredient_schemas.IngredientOut:
    """
    Update an ingredient by ID.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
    try:
        updated_ingredient: Ingredient = ingredient_service.update_ingredient(
            ingredient_id=ingredient_id,
            name=ingredient.name,
            description=ingredient.description,
            recipe_id=ingredient.recipe_id,
        )
        return ingredient_schemas.IngredientOut.model_validate(updated_ingredient)
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
async def delete_ingredient(
    ingredient_id: int,
    ingredient_service: Ingredient_Service,
    authenticated_user: AuthenticatedUser,
) -> Detail:
    """
    Delete an ingredient by ID.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
    try:
        ingredient_service.delete_ingredient(ingredient_id=ingredient_id)
        return Detail(detail=f"Ingredient with ID {ingredient_id} has been deleted.")
    except errors.IngredientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
