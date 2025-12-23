from contextlib import asynccontextmanager

from fastapi import FastAPI

from docuisine import routes
from docuisine.db.database import engine
from docuisine.db.models.base import Base


@asynccontextmanager
async def on_startup(app: FastAPI):
    # Create database tables when the application starts
    try:
        Base.metadata.create_all(bind=engine)
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


app.include_router(routes.root.router)
app.include_router(routes.auth.router)
app.include_router(routes.user.router)
app.include_router(routes.category.router)
app.include_router(routes.store.router)
app.include_router(routes.ingredient.router)
app.include_router(routes.recipe.router)
app.include_router(routes.health.router)
