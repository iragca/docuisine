from functools import cached_property
from hashlib import md5
from io import BytesIO

from botocore import client
from PIL import Image, ImageFile

from docuisine.schemas.enums import ImageFormat
from docuisine.utils.errors import UnsupportedImageFormatError


class ImageService:
    def __init__(
        self,
        s3: client.BaseClient,
    ):
        """
        Initialize the ImageService with S3 client.

        Parameters
        ----------
        s3 : client.BaseClient
            The S3 client for interacting with the S3 storage.
        """
        self.s3 = s3

    def upload_image(self, image: bytes) -> str:
        """
        Upload an image to the S3 bucket.

        Parameters
        ----------
        image_bytes : bytes
            The image data in bytes.

        Returns
        -------
        str
            The path of the uploaded image within the S3 bucket.
        """
        buffer = BytesIO(image)
        buffer.seek(0)

        format = self._determine_format(buffer)
        self._validate_format(format)
        image_name = self._build_image_name(image, format)
        buffer.seek(0)

        self.s3.upload_fileobj(
            Bucket=self.s3.bucket_name,
            Key=image_name,
            Fileobj=buffer,
            ExtraArgs={"ContentType": f"image/{format}"},
        )
        return image_name

    @staticmethod
    def _build_image_name(image_bytes: bytes, format: str) -> str:
        """
        Build a unique image name based on the MD5 hash of the image bytes.
        Parameters
        ----------
        image_bytes : bytes
            The image data in bytes.
        format : str
            The image format.

        Returns
        -------
        str
            The generated image name.
        """
        image_hash = md5(image_bytes).hexdigest()
        return f"{image_hash}.{format}"

    @staticmethod
    def _determine_format(image: BytesIO) -> str:
        """
        Determine the format of the given image bytes.


        Parameters
        ----------
        image : BytesIO
            The image data in bytes.

        Returns
        -------
        str
            The format of the image.
        """
        ## Open regardless of truncated images
        ImageFile.LOAD_TRUNCATED_IMAGES = True  # type: ignore
        with Image.open(image) as img:
            return img.format.lower()

    def _validate_format(self, format: str) -> None:
        """
        Validate if the given image format is supported.

        Parameters
        ----------
        format : str
            The image format to validate.

        Raises
        ------
        UnsupportedImageFormatError
            If the image format is not supported.
        """
        if format.lower() not in self._supported_formats:
            raise UnsupportedImageFormatError(format=format.lower())

    @cached_property
    def _supported_formats(self) -> set[str]:
        """
        Return the set of supported image formats.
        """
        return {fmt.value.lower() for fmt in ImageFormat}
