from fastapi import FastAPI

from docuisine.routes import health, user

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(user.router)
app.include_router(health.router)
