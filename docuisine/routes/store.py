from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import Store
from docuisine.dependencies import Store_Service
from docuisine.schemas.common import Detail
from docuisine.schemas.store import StoreCreate, StoreOut, StoreUpdate
from docuisine.utils import errors

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[StoreOut])
async def get_stores(store_service: Store_Service) -> list[StoreOut]:
    """Get all stores."""
    stores: list[Store] = store_service.get_all_stores()
    return [StoreOut.model_validate(store) for store in stores]


@router.get(
    "/{store_id}",
    status_code=status.HTTP_200_OK,
    response_model=StoreOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_store(store_id: int, store_service: Store_Service) -> StoreOut:
    """Get a store by ID."""
    try:
        store: Store = store_service.get_store(store_id=store_id)
        return StoreOut.model_validate(store)
    except errors.StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=StoreOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_store(store: StoreCreate, store_service: Store_Service) -> StoreOut:
    """Create a new store."""
    try:
        new_store: Store = store_service.create_store(
            name=store.name,
            address=store.address,
            longitude=store.longitude,
            latitude=store.latitude,
            phone=store.phone,
            website=store.website,
            description=store.description,
        )
        return StoreOut.model_validate(new_store)
    except errors.StoreExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.put(
    "/{store_id}",
    status_code=status.HTTP_200_OK,
    response_model=StoreOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_store(
    store_id: int, store: StoreUpdate, store_service: Store_Service
) -> StoreOut:
    """Update a store by ID."""
    try:
        updated: Store = store_service.update_store(
            store_id=store_id,
            name=store.name,
            address=store.address,
            longitude=store.longitude,
            latitude=store.latitude,
            phone=store.phone,
            website=store.website,
            description=store.description,
        )
        return StoreOut.model_validate(updated)
    except errors.StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except errors.StoreExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.delete(
    "/{store_id}",
    status_code=status.HTTP_200_OK,
    response_model=Detail,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def delete_store(store_id: int, store_service: Store_Service) -> Detail:
    """Delete a store by ID."""
    try:
        store_service.delete_store(store_id=store_id)
        return Detail(detail=f"Store with ID {store_id} has been deleted.")
    except errors.StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
