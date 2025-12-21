from contextlib import asynccontextmanager

from fastapi import FastAPI

from docuisine.db.database import engine
from docuisine.db.models.base import Base
from docuisine.routes import category, health, ingredient, root, user


@asynccontextmanager
async def on_startup(app: FastAPI):
    # Create database tables when the application starts
    try:
        Base.metadata.create_all(bind=engine)
        yield
    finally:
        # Dispose of the database engine when the application shuts down
        await engine.dispose()


app = FastAPI(lifespan=on_startup)


app.include_router(root.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(ingredient.router)
app.include_router(health.router)
