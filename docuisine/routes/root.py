from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint.

    Access Level: Public
    """
    return "Hello, from Docuisine!"
