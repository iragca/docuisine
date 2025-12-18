from contextlib import asynccontextmanager

from fastapi import FastAPI

from docuisine.db.models.base import Base
from docuisine.routes import health, root, user


@asynccontextmanager
async def on_startup(app: FastAPI):
    # Create database tables when the application starts
    Base.metadata.create_all(bind=app.state._engine)


app = FastAPI(lifespan=on_startup)


app.include_router(root.router)
app.include_router(user.router)
app.include_router(health.router)
