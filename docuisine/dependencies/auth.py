from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from docuisine.db.models import User
from docuisine.utils import errors

from .services import User_Service

OAuth2_Scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


AuthToken = Annotated[str, Depends(OAuth2_Scheme)]
AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_current_user_token(token: AuthToken, user_service: User_Service):
    try:
        user = user_service.authorize_user(token=token)
    except errors.InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


AuthenticatedUser = Annotated[User, Depends(get_current_user_token)]
