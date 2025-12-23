from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import User
from docuisine.dependencies import AuthenticatedUser, User_Service
from docuisine.schemas.common import Detail
from docuisine.schemas.enums import Role
from docuisine.schemas.user import UserCreate, UserOut, UserUpdateEmail, UserUpdatePassword
from docuisine.utils import errors

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserOut])
async def get_users(user_service: User_Service) -> list[UserOut]:
    """
    Get all users.

    Access Level: Public
    """
    users: list[User] = user_service.get_all_users()
    return [UserOut.model_validate(user) for user in users]


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_user(user_id: int, user_service: User_Service) -> UserOut:
    """
    Get a user by ID.

    Access Level: Public
    """
    try:
        user: User = user_service.get_user(user_id=user_id)
        return UserOut.model_validate(user)
    except errors.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_user(user: UserCreate, user_service: User_Service) -> UserOut:
    """
    Create a new user.

    Access Level: Public
    """
    try:
        new_user: User = user_service.create_user(user.username, user.password, user.email)
        return UserOut.model_validate(new_user)
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
    if authenticated_user.role not in {Role.ADMIN, Role.USER}:
        raise errors.ForbiddenAccessError
    if authenticated_user.id != user_id:
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
    response_model=UserOut,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Detail},
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_user_email(
    user: UserUpdateEmail, user_service: User_Service, authenticated_user: AuthenticatedUser
) -> UserOut:
    """
    Update user email.

    Access Level: Admin, User
    """
    if authenticated_user.role not in {Role.ADMIN, Role.USER}:
        raise errors.ForbiddenAccessError
    if authenticated_user.id != user.id:
        raise errors.ForbiddenAccessError
    try:
        updated_user: User = user_service.update_user_email(user_id=user.id, new_email=user.email)
        return UserOut.model_validate(updated_user)
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
    response_model=UserOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Detail},
    },
)
async def update_user_password(
    user: UserUpdatePassword, user_service: User_Service, authenticated_user: AuthenticatedUser
) -> UserOut:
    """
    Update user password.

    Access Level: Admin, User
    """
    if authenticated_user.role not in {Role.ADMIN, Role.USER}:
        raise errors.ForbiddenAccessError
    if authenticated_user.id != user.id:
        raise errors.ForbiddenAccessError
    try:
        updated_user: User = user_service.update_user_password(
            user_id=user.id, old_password=user.old_password, new_password=user.new_password
        )
        return UserOut.model_validate(updated_user)
    except errors.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
