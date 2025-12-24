from fastapi import APIRouter, status

from docuisine.dependencies import AuthenticatedUser, Image_Service
from docuisine.schemas.annotations import ImageUpload
from docuisine.schemas.common import Detail
from docuisine.schemas.enums import Role
from docuisine.schemas.image import ImageSet
from docuisine.utils import errors

router = APIRouter(prefix="/image", tags=["Image"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_403_FORBIDDEN: {"model": Detail}},
    response_model=ImageSet,
)
async def upload_image(
    authenticated_user: AuthenticatedUser, image_service: Image_Service, image: ImageUpload
) -> ImageSet:
    """
    Upload images.

    Access Level: Admin
    """
    if authenticated_user.role not in {Role.ADMIN}:
        raise errors.ForbiddenAccessError
    return image_service.upload_image(await image.read())
