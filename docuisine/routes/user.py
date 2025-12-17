from fastapi import APIRouter, HTTPException, status

from docuisine.db import db
from docuisine.db.models import User
from docuisine.schemas.user import UserCreate, UserOut, UserRead
from docuisine.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserOut])
def get_users() -> list[UserOut]:
    user_service = UserService(db_session=db)
    users: list[dict] = [user.as_dict() for user in user_service.get_all_users()]
    return [UserOut(id=user["id"], email=user["email"]) for user in users]


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(user_id: int):
    user_service = UserService(db_session=db)
    user: User = user_service.get_user(UserRead(id=user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )

    return UserOut(**user.as_dict())


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate):
    user_service = UserService(db_session=db)
    new_user: User = user_service.create_user(user=user)
    return UserOut(**new_user.as_dict())
