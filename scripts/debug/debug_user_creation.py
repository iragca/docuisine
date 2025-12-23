from fastapi import HTTPException, status

from docuisine.db.models import User
from docuisine.dependencies.db import get_db_session
from docuisine.dependencies.services import User_Service, get_user_service
from docuisine.schemas.auth import Token
from docuisine.schemas.enums import TokenType
from docuisine.utils import errors


def login(form_data: dict, user_service: User_Service) -> Token:
    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user = user_service.authenticate_user(
            username=form_data["username"], password=form_data["password"]
        )
    except errors.UserNotFoundError:
        raise invalid_credentials_exception
    if not user:
        raise invalid_credentials_exception

    if isinstance(user, User):
        access_token = user_service.create_access_token(user)
        return Token(access_token=access_token, token_type=TokenType.BEARER)

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred during authentication.",
    )


login({"username": "alice", "password": "hashed_password_1P!"}, get_user_service(get_db_session()))
