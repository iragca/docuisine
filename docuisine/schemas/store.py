from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StoreCreate(BaseModel):
    name: str = Field(..., description="The store name", examples=["Grocery Mart"])
    address: str = Field(..., description="The store address", examples=["123 Main St"])
    longitude: Optional[float] = Field(
        None, description="Longitude coordinate", examples=[-122.4194]
    )
    latitude: Optional[float] = Field(None, description="Latitude coordinate", examples=[37.7749])
    phone: Optional[str] = Field(None, description="Phone number", examples=["555-1234"])
    website: Optional[str] = Field(
        None, description="Website URL", examples=["https://example.com"]
    )
    description: Optional[str] = Field(
        None, description="Store description", examples=["Local grocery store"]
    )


class StoreUpdate(BaseModel):
    name: Optional[str] = Field(None, description="The store name")
    address: Optional[str] = Field(None, description="The store address")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[str] = Field(None, description="Website URL")
    description: Optional[str] = Field(None, description="Store description")


class StoreOut(BaseModel):
    id: int = Field(..., description="The store's unique identifier", examples=[1])
    name: str = Field(..., description="The store name", examples=["Grocery Mart"])
    address: str = Field(..., description="The store address", examples=["123 Main St"])
    longitude: Optional[float] = Field(
        None, description="Longitude coordinate", examples=[-122.4194]
    )
    latitude: Optional[float] = Field(None, description="Latitude coordinate", examples=[37.7749])
    phone: Optional[str] = Field(None, description="Phone number", examples=["+31555-1234"])
    website: Optional[str] = Field(
        None, description="Website URL", examples=["https://example.com"]
    )
    description: Optional[str] = Field(None, description="Store description")

    model_config = ConfigDict(from_attributes=True)
