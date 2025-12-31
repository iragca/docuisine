from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status

from docuisine.db.models import User
from docuisine.dependencies import AuthenticatedUser, Image_Service, User_Service
from docuisine.schemas import user as user_schemas
from docuisine.schemas.annotations import ImageUpload
from docuisine.schemas.common import Detail
from docuisine.schemas.enums import Role
from docuisine.utils import errors
from docuisine.utils.validation import validate_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[user_schemas.UserOut])
async def get_users(user_service: User_Service) -> list[user_schemas.UserOut]:
    """
    Get all users.

    Access Level: Public
    """
    users: list[User] = user_service.get_all_users()
    return [user_schemas.UserOut.model_validate(user) for user in users]


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_user(user_id: int, user_service: User_Service) -> user_schemas.UserOut:
    """
    Get a user by ID.

    Access Level: Public
    """
    try:
        user: User = user_service.get_user(user_id=user_id)
        return user_schemas.UserOut.model_validate(user)
    except errors.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schemas.UserOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_user(
    user: user_schemas.UserCreate, user_service: User_Service
) -> user_schemas.UserOut:
    """
    Create a new user.

    Access Level: Public
    """
    try:
        new_user: User = user_service.create_user(user.username, user.password, user.email)
        return user_schemas.UserOut.model_validate(new_user)
    except errors.UserExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=Detail,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def delete_user(
    user_id: int, user_service: User_Service, authenticated_user: AuthenticatedUser
) -> Detail:
    """
    Delete a user by ID.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
    if (authenticated_user.id != user_id) and (authenticated_user.role != Role.ADMIN):
        raise errors.ForbiddenAccessError
    try:
        user_service.delete_user(user_id=user_id)
        return Detail(detail=f"User with ID {user_id} has been deleted.")
    except errors.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.put(
    "/email",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserOut,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Detail},
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_user_email(
    user: user_schemas.UserUpdateEmail,
    user_service: User_Service,
    authenticated_user: AuthenticatedUser,
) -> user_schemas.UserOut:
    """
    Update user email.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
    if authenticated_user.id != user.id:
        raise errors.ForbiddenAccessError
    try:
        updated_user: User = user_service.update_user_email(user_id=user.id, new_email=user.email)
        return user_schemas.UserOut.model_validate(updated_user)
    except errors.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except errors.DuplicateEmailError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.put(
    "/password",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Detail},
    },
)
async def update_user_password(
    user: user_schemas.UserUpdatePassword,
    user_service: User_Service,
    authenticated_user: AuthenticatedUser,
) -> user_schemas.UserOut:
    """
    Update user password.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
    if authenticated_user.id != user.id:
        raise errors.ForbiddenAccessError
    try:
        updated_user: User = user_service.update_user_password(
            user_id=user.id, old_password=user.old_password, new_password=user.new_password
        )
        return user_schemas.UserOut.model_validate(updated_user)
    except errors.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except errors.InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.put(
    "/img",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserOut,
)
async def update_user_img(
    user_id: Annotated[int, Form()],
    user_service: User_Service,
    authenticated_user: AuthenticatedUser,
    fileb: ImageUpload,
    image_service: Image_Service,
) -> user_schemas.UserOut:
    """
    Update the current user's profile.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
    if authenticated_user.id != user_id:
        raise errors.ForbiddenAccessError

    try:
        image_set = image_service.upload_image(await fileb.read())

        updated_user = user_service.update_user_img(
            user_id=user_id, img=image_set.original, preview_img=image_set.preview
        )
        return updated_user

    except errors.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
