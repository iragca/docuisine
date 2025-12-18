from fastapi import FastAPI

from docuisine.routes import health, root, user

app = FastAPI()


app.include_router(root.router)
app.include_router(user.router)
app.include_router(health.router)
