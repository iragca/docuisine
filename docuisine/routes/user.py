from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import User
from docuisine.schemas.annotations import DB_session
from docuisine.schemas.user import UserCreate, UserOut
from docuisine.services import UserService
from docuisine.utils import errors

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserOut])
def get_users(db: DB_session) -> list[UserOut]:
    user_service = UserService(db_session=db)
    users: list[User] = user_service.get_all_users()
    return [UserOut.model_validate(user) for user in users]


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(user_id: int, db: DB_session) -> UserOut:
    user_service = UserService(db_session=db)
    try:
        user: User = user_service.get_user(user_id=user_id)
        return UserOut.model_validate(user)
    except errors.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: DB_session) -> UserOut:
    user_service = UserService(db_session=db)
    try:
        new_user: User = user_service.create_user(user.email, user.password)
        return UserOut.model_validate(new_user)
    except errors.UserExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
