from pydantic import BaseModel


class S3Config(BaseModel):
    """
    Configuration settings for S3 storage.

    Attributes
    ----------
    endpoint_url : str
        The endpoint URL of the S3 service.
    access_key : str
        The access key for S3 authentication.
    secret_key : str
        The secret key for S3 authentication.
    """

    endpoint_url: str
    access_key: str
    secret_key: str
