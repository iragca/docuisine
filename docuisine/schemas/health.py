from pydantic import BaseModel, Field

from .common import CommitHash, Status, Version


class HealthCheck(BaseModel):
    status: Status = Field(..., example=Status.HEALTHY)
    commit_hash: CommitHash = Field(..., example="a1b2c3d")
    version: Version = Field(..., example="1.0.0")
