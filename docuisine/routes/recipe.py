from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import Recipe
from docuisine.dependencies import AuthenticatedUser, Recipe_Service
from docuisine.schemas.common import Detail
from docuisine.schemas.enums import Role
from docuisine.schemas.recipe import RecipeCreate, RecipeOut, RecipeUpdate
from docuisine.utils import errors

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RecipeOut])
async def get_recipes(recipe_service: Recipe_Service) -> list[RecipeOut]:
    """
    Get all recipes.

    Access Level: Public
    """
    recipes: list[Recipe] = recipe_service.get_all_recipes()
    return [RecipeOut.model_validate(recipe) for recipe in recipes]


@router.get(
    "/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[RecipeOut],
)
async def get_recipes_by_user(user_id: int, recipe_service: Recipe_Service) -> list[RecipeOut]:
    """
    Get all recipes created by a specific user.

    Access Level: Public
    """
    recipes: list[Recipe] = recipe_service.get_recipes_by_user(user_id=user_id)
    return [RecipeOut.model_validate(recipe) for recipe in recipes]


@router.get(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK,
    response_model=RecipeOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_recipe(recipe_id: int, recipe_service: Recipe_Service) -> RecipeOut:
    """
    Get a recipe by ID.

    Access Level: Public
    """
    try:
        recipe: Recipe = recipe_service.get_recipe(recipe_id=recipe_id)
        return RecipeOut.model_validate(recipe)
    except errors.RecipeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RecipeOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_recipe(
    recipe: RecipeCreate,
    recipe_service: Recipe_Service,
    authenticated_user: AuthenticatedUser,
) -> RecipeOut:
    """
    Create a new recipe.

    Access Level: Admin, User
    """
    if authenticated_user.role not in {Role.ADMIN, Role.USER}:
        raise errors.ForbiddenAccessError
    try:
        new_recipe: Recipe = recipe_service.create_recipe(
            user_id=authenticated_user.id,
            name=recipe.name,
            cook_time_sec=recipe.cook_time_sec,
            prep_time_sec=recipe.prep_time_sec,
            non_blocking_time_sec=recipe.non_blocking_time_sec,
            servings=recipe.servings,
            description=recipe.description,
        )
        return RecipeOut.model_validate(new_recipe)
    except errors.RecipeExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.put(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK,
    response_model=RecipeOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_recipe(
    recipe_id: int,
    recipe: RecipeUpdate,
    recipe_service: Recipe_Service,
    authenticated_user: AuthenticatedUser,
) -> RecipeOut:
    """
    Update a recipe by ID.

    Access Level: Admin, User
    """
    if authenticated_user.role not in {Role.ADMIN, Role.USER}:
        raise errors.ForbiddenAccessError
    if authenticated_user.role == Role.USER:
        if recipe_id not in {r.id for r in authenticated_user.recipes}:
            raise errors.ForbiddenAccessError
    try:
        updated: Recipe = recipe_service.update_recipe(
            recipe_id=recipe_id,
            name=recipe.name,
            cook_time_sec=recipe.cook_time_sec,
            prep_time_sec=recipe.prep_time_sec,
            non_blocking_time_sec=recipe.non_blocking_time_sec,
            servings=recipe.servings,
            description=recipe.description,
        )
        return RecipeOut.model_validate(updated)
    except errors.RecipeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except errors.RecipeExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK,
    response_model=Detail,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def delete_recipe(
    recipe_id: int, recipe_service: Recipe_Service, authenticated_user: AuthenticatedUser
) -> Detail:
    """
    Delete a recipe by ID.

    Access Level: Admin, User
    """
    if authenticated_user.role not in {Role.ADMIN, Role.USER}:
        raise errors.ForbiddenAccessError
    if authenticated_user.role == Role.USER:
        if recipe_id not in {r.id for r in authenticated_user.recipes}:
            raise errors.ForbiddenAccessError
    try:
        recipe_service.delete_recipe(recipe_id=recipe_id)
        return Detail(detail=f"Recipe with ID {recipe_id} has been deleted.")
    except errors.RecipeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
