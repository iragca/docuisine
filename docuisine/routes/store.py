from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import Store
from docuisine.dependencies import AuthenticatedUser, Store_Service
from docuisine.schemas import store as store_schemas
from docuisine.schemas.common import Detail
from docuisine.utils import errors
from docuisine.utils.validation import validate_role

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[store_schemas.StoreOut])
async def get_stores(store_service: Store_Service) -> list[store_schemas.StoreOut]:
    """
    Get all stores.

    Access Level: Public
    """
    stores: list[Store] = store_service.get_all_stores()
    return [store_schemas.StoreOut.model_validate(store) for store in stores]


@router.get(
    "/{store_id}",
    status_code=status.HTTP_200_OK,
    response_model=store_schemas.StoreOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": Detail}},
)
async def get_store(store_id: int, store_service: Store_Service) -> store_schemas.StoreOut:
    """
    Get a store by ID.

    Access Level: Public
    """
    try:
        store: Store = store_service.get_store(store_id=store_id)
        return store_schemas.StoreOut.model_validate(store)
    except errors.StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=store_schemas.StoreOut,
    responses={status.HTTP_409_CONFLICT: {"model": Detail}},
)
async def create_store(
    store: store_schemas.StoreCreate,
    store_service: Store_Service,
    authenticated_user: AuthenticatedUser,
) -> store_schemas.StoreOut:
    """
    Create a new store.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
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
        return store_schemas.StoreOut.model_validate(new_store)
    except errors.StoreExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.put(
    "/{store_id}",
    status_code=status.HTTP_200_OK,
    response_model=store_schemas.StoreOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Detail},
        status.HTTP_409_CONFLICT: {"model": Detail},
    },
)
async def update_store(
    store_id: int,
    store: store_schemas.StoreUpdate,
    store_service: Store_Service,
    authenticated_user: AuthenticatedUser,
) -> store_schemas.StoreOut:
    """
    Update a store by ID.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
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
        return store_schemas.StoreOut.model_validate(updated)
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
async def delete_store(
    store_id: int, store_service: Store_Service, authenticated_user: AuthenticatedUser
) -> Detail:
    """
    Delete a store by ID.

    Access Level: Admin, User
    """
    validate_role(authenticated_user.role, "au")
    try:
        store_service.delete_store(store_id=store_id)
        return Detail(detail=f"Store with ID {store_id} has been deleted.")
    except errors.StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
