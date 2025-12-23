from typing import Annotated

from fastapi import Depends

from docuisine.core.config import env
from docuisine.schemas.auth import JWTConfig
from docuisine.schemas.enums import JWTAlgorithm
from docuisine.services import (
    CategoryService,
    IngredientService,
    RecipeService,
    StoreService,
    UserService,
)

from .db import DB_Session


def get_user_service(
    db_session: DB_Session,
) -> UserService:
    return UserService(
        db_session,
        jwt_config=JWTConfig(
            secret_key=env.JWT_SECRET_KEY,
            algorithm=JWTAlgorithm(value=env.JWT_ALGORITHM),
            access_token_expire_minutes=env.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )


def get_category_service(
    db_session: DB_Session,
) -> CategoryService:
    return CategoryService(db_session)


def get_ingredient_service(
    db_session: DB_Session,
) -> IngredientService:
    return IngredientService(db_session)


def get_store_service(
    db_session: DB_Session,
) -> StoreService:
    return StoreService(db_session)


def get_recipe_service(
    db_session: DB_Session,
) -> RecipeService:
    return RecipeService(db_session)


User_Service = Annotated[UserService, Depends(get_user_service)]
Category_Service = Annotated[CategoryService, Depends(get_category_service)]
Ingredient_Service = Annotated[IngredientService, Depends(get_ingredient_service)]
Store_Service = Annotated[StoreService, Depends(get_store_service)]
Recipe_Service = Annotated[RecipeService, Depends(get_recipe_service)]
