from fastapi import APIRouter

from docuisine.core.config import env
from docuisine.schemas import HealthCheck, Status

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthCheck)
def health_check():
    return HealthCheck(
        status=Status.HEALTHY,
        commit_hash=env.COMMIT_HASH,
        version=env.VERSION,
    )
