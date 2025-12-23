from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import Category
from docuisine.dependencies import AuthenticatedUser, Category_Service
from docuisine.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from docuisine.schemas.common import Detail
from docuisine.schemas.enums import Role
from docuisine.utils import errors

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CategoryOut])
async def get_categories(category_service: Category_Service) -> list[CategoryOut]:
    """
    Get all categories.

    Access Level: Public
    """
    categories: list[Category] = category_service.get_all_categories()
    return [CategoryOut.model_validate(category) for category in categories]


@router.get(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_category(category_id: int, category_service: Category_Service) -> CategoryOut:
    """
    Get a category by ID.

    Access Level: Public
    """
    try:
        category: Category = category_service.get_category(category_id=category_id)
        return CategoryOut.model_validate(category)
    except errors.CategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_category(
    category: CategoryCreate,
    category_service: Category_Service,
    authenticated_user: AuthenticatedUser,
) -> CategoryOut:
    """
    Create a new category.

    Access Level: Admin
    """
    if authenticated_user.role != Role.ADMIN:
        raise errors.ForbiddenAccessError
    try:
        new_category: Category = category_service.create_category(
            name=category.name, description=category.description
        )
        return CategoryOut.model_validate(new_category)
    except errors.CategoryExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.put(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryOut,
    responses={
        status.HTTP_403_FORBIDDEN: {"model": Detail},
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    category_service: Category_Service,
    authenticated_user: AuthenticatedUser,
) -> CategoryOut:
    """
    Update an existing category.

    Access Level: Admin
    """
    if authenticated_user.role != Role.ADMIN:
        raise errors.ForbiddenAccessError
    try:
        updated_category: Category = category_service.update_category(
            category_id=category_id, name=category.name, description=category.description
        )
        return CategoryOut.model_validate(updated_category)
    except errors.CategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except errors.CategoryExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=Detail,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def delete_category(
    category_id: int, category_service: Category_Service, authenticated_user: AuthenticatedUser
) -> Detail:
    """
    Delete a category by ID.

    Access Level: Admin
    """
    if authenticated_user.role != Role.ADMIN:
        raise errors.ForbiddenAccessError
    try:
        category_service.delete_category(category_id=category_id)
        return Detail(detail=f"Category with ID {category_id} has been deleted.")
    except errors.CategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
