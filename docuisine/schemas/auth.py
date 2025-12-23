from typing import Optional

from pydantic import BaseModel, Field

from .enums import JWTAlgorithm, TokenType


class Token(BaseModel):
    """
    Schema for authentication tokens.
    """

    access_token: str
    token_type: TokenType


class JWTConfig(BaseModel):
    """
    Configuration settings for JWT authentication.

    Attributes
    ----------
    secret_key : str
        The secret key used to sign the JWT tokens.
    algorithm : str
        The algorithm used for signing the JWT tokens.
    access_token_expire_minutes : Optional[int]
        The expiration time for access tokens in minutes. Defaults to 525600 (1 year).
    """

    secret_key: str
    algorithm: JWTAlgorithm = Field(default=JWTAlgorithm.HS256)
    access_token_expire_minutes: Optional[int] = Field(default=60 * 24 * 365, ge=1)
