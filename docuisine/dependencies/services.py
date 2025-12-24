from typing import Annotated
from urllib.parse import urljoin

from fastapi import Depends

from docuisine import services
from docuisine.core.config import env
from docuisine.schemas.auth import JWTConfig
from docuisine.schemas.enums import JWTAlgorithm

from .db import DB_Session
from .storage import S3_Client


def get_user_service(
    db_session: DB_Session,
) -> services.UserService:
    return services.UserService(
        db_session,
        jwt_config=JWTConfig(
            secret_key=env.JWT_SECRET_KEY,
            algorithm=JWTAlgorithm(value=env.JWT_ALGORITHM),
            access_token_expire_minutes=env.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
        image_host=urljoin(env.S3_ENDPOINT_URL, env.S3_BUCKET_NAME),
    )


def get_category_service(
    db_session: DB_Session,
) -> services.CategoryService:
    return services.CategoryService(db_session)


def get_ingredient_service(
    db_session: DB_Session,
) -> services.IngredientService:
    return services.IngredientService(db_session)


def get_store_service(
    db_session: DB_Session,
) -> services.StoreService:
    return services.StoreService(db_session)


def get_recipe_service(
    db_session: DB_Session,
) -> services.RecipeService:
    return services.RecipeService(db_session)


def get_image_service(
    s3_client: S3_Client,
) -> services.ImageService:
    return services.ImageService(s3=s3_client)


User_Service = Annotated[services.UserService, Depends(get_user_service)]
Category_Service = Annotated[services.CategoryService, Depends(get_category_service)]
Ingredient_Service = Annotated[services.IngredientService, Depends(get_ingredient_service)]
Store_Service = Annotated[services.StoreService, Depends(get_store_service)]
Recipe_Service = Annotated[services.RecipeService, Depends(get_recipe_service)]
Image_Service = Annotated[services.ImageService, Depends(get_image_service)]
