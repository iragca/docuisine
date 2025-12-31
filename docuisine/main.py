from contextlib import asynccontextmanager
import json

from botocore.exceptions import ClientError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from docuisine import routes
from docuisine.db.database import engine
from docuisine.db.models.base import Base
from docuisine.db.storage import s3_config, s3_storage

## Define S3 bucket policy to allow public read access to objects
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::docuisine-images/*"],
        }
    ],
}


@asynccontextmanager
async def on_startup(app: FastAPI):
    """
    Application startup event handler.

    Notes
    -----
    This startup event runs when the application starts
    It does two things:
    1. Creates all database tables based on the defined models
    2. Ensures the S3 bucket for image storage exists with the correct policy
    """
    try:
        Base.metadata.create_all(bind=engine)
        try:
            s3_storage.head_bucket(Bucket=s3_config.bucket_name)
        except ClientError:
            s3_storage.create_bucket(Bucket=s3_config.bucket_name)
            s3_storage.put_bucket_policy(Bucket=s3_config.bucket_name, Policy=json.dumps(policy))
        yield
    finally:
        # Dispose of the database engine when the application shuts down
        if not callable(hasattr(engine, "dispose")):
            raise RuntimeError(
                "Database engine is not initialized. "
                "This is likely because the provided DATABASE_URL is wrong."
            )
        else:
            await engine.dispose()


app = FastAPI(lifespan=on_startup)


app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.root.router)
app.include_router(routes.auth.router)
app.include_router(routes.user.router)
app.include_router(routes.category.router)
app.include_router(routes.store.router)
app.include_router(routes.ingredient.router)
app.include_router(routes.recipe.router)
app.include_router(routes.health.router)
app.include_router(routes.image.router)
