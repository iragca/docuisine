from pydantic import BaseModel, Field


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
    bucket_name : str
        The name of the S3 bucket to use. Default is "docuisine-images".
    """

    endpoint_url: str
    access_key: str
    secret_key: str
    bucket_name: str = "docuisine-images"


class ImageSet(BaseModel):
    """
    Represents a set of images including the original and its preview.
    """

    ORIGINAL: str = Field(..., description="Original image", examples=["123940712123.jpg"])
    PREVIEW: str = Field(..., description="Preview image", examples=["1412312341234.jpg"])
