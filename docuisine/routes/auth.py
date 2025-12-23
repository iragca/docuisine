from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import User
from docuisine.dependencies import AuthForm
from docuisine.dependencies.services import User_Service
from docuisine.schemas.auth import Token
from docuisine.schemas.common import Detail
from docuisine.schemas.enums import TokenType
from docuisine.utils import errors

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    response_model=Token,
    summary="User Login",
    description="Authenticate user and return an access token.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": Detail},
        status.HTTP_404_NOT_FOUND: {"model": Detail},
    },
)
async def login(form_data: AuthForm, user_service: User_Service) -> Token:
    """
    Authenticate user and return an access token.

    Access Level: Public
    """
    try:
        user = user_service.authenticate_user(
            username=form_data.username, password=form_data.password
        )
    except errors.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except errors.InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )

    if isinstance(user, User):
        access_token = user_service.create_access_token(user)
        return Token(access_token=access_token, token_type=TokenType.BEARER)

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred during authentication.",
    )
