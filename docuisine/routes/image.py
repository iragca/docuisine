from fastapi import APIRouter, status

from docuisine.dependencies import AuthenticatedUser, Image_Service
from docuisine.schemas import image as image_schemas
from docuisine.schemas.annotations import ImageUpload
from docuisine.schemas.common import Detail
from docuisine.utils.validation import validate_role

router = APIRouter(prefix="/image", tags=["Image"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_403_FORBIDDEN: {"model": Detail}},
    response_model=image_schemas.ImageSet,
)
async def upload_image(
    authenticated_user: AuthenticatedUser, image_service: Image_Service, image: ImageUpload
) -> image_schemas.ImageSet:
    """
    Upload images.

    Access Level: Admin
    """
    validate_role(authenticated_user.role, "a")
    return image_service.upload_image(await image.read())
