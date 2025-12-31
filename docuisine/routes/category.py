from typing import Optional

from fastapi import APIRouter, Form, HTTPException, status

from docuisine.db.models import Category
from docuisine.dependencies import AuthenticatedUser, Category_Service, Image_Service
from docuisine.schemas import category as category_schemas
from docuisine.schemas.annotations import CategoryName, ImageUpload
from docuisine.schemas.common import Detail
from docuisine.utils import errors
from docuisine.utils.validation import validate_role

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[category_schemas.CategoryOut])
async def get_categories(category_service: Category_Service) -> list[category_schemas.CategoryOut]:
    """
    Get all categories.

    Access Level: Public
    """
    categories: list[Category] = category_service.get_all_categories()
    return [category_schemas.CategoryOut.model_validate(category) for category in categories]


@router.get(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=category_schemas.CategoryOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_category(
    category_id: int, category_service: Category_Service
) -> category_schemas.CategoryOut:
    """
    Get a category by ID.

    Access Level: Public
    """
    try:
        category: Category = category_service.get_category(category_id=category_id)
        return category_schemas.CategoryOut.model_validate(category)
    except errors.CategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=category_schemas.CategoryOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_category(
    category_service: Category_Service,
    authenticated_user: AuthenticatedUser,
    image_service: Image_Service,
    name: CategoryName,
    image: Optional[ImageUpload] = None,
    description: Optional[str] = Form(
        None,
        description="The category description",
        examples=["Sweet dishes and treats"],
    ),
) -> category_schemas.CategoryOut:
    """
    Create a new category.

    Access Level: Admin
    """
    validate_role(authenticated_user.role, "a")
    if image is not None:
        image_set = image_service.upload_image(await image.read())

    try:
        new_category: Category = category_service.create_category(
            name=name,
            description=description,
            img=image_set.original if image is not None else None,
            preview_img=image_set.preview if image is not None else None,
        )
        return category_schemas.CategoryOut.model_validate(new_category)
    except errors.CategoryExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=category_schemas.CategoryOut,
    responses={
        status.HTTP_403_FORBIDDEN: {"model": Detail},
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_category(
    category: category_schemas.CategoryUpdate,
    category_service: Category_Service,
    authenticated_user: AuthenticatedUser,
) -> category_schemas.CategoryOut:
    """
    Update an existing category.

    Access Level: Admin
    """
    validate_role(authenticated_user.role, "a")
    try:
        updated_category: Category = category_service.update_category(
            category_id=category.id, name=category.name, description=category.description
        )
        return category_schemas.CategoryOut.model_validate(updated_category)
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
    validate_role(authenticated_user.role, "a")
    try:
        category_service.delete_category(category_id=category_id)
        return Detail(detail=f"Category with ID {category_id} has been deleted.")
    except errors.CategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
