from typing import Union

from fastapi import FastAPI

from .schemas import HealthCheck

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/health", response_model=HealthCheck)
def health_check():
    return HealthCheck(status="healthy")
