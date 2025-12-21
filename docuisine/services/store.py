from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from docuisine.db.models import Store
from docuisine.utils.errors.store import StoreExistsError, StoreNotFoundError


class StoreService:
    def __init__(self, db_session: Session):
        self.db_session: Session = db_session

    def create_store(
        self,
        name: str,
        address: str,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Store:
        """
        Create a new store in the database.

        Parameters
        ----------
        name : str
            The name of the store.
        address : str
            The address of the store.
        longitude : Optional[float]
            Longitude coordinate. Default is None.
        latitude : Optional[float]
            Latitude coordinate. Default is None.
        phone : Optional[str]
            Phone number. Default is None.
        website : Optional[str]
            Website URL. Default is None.
        description : Optional[str]
            Store description. Default is None.

        Returns
        -------
        Store
            The newly created `Store` instance.

        Raises
        ------
        StoreExistsError
            If a store with the same name already exists.
        """
        new_store = Store(
            name=name,
            address=address,
            longitude=longitude,
            latitude=latitude,
            phone=phone,
            website=website,
            description=description,
        )
        try:
            self.db_session.add(new_store)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise StoreExistsError(name)
        return new_store

    def get_store(self, store_id: Optional[int] = None, name: Optional[str] = None) -> Store:
        """
        Retrieve a store by ID or name.

        Parameters
        ----------
        store_id : Optional[int]
            The unique ID of the store.
        name : Optional[str]
            The name of the store.

        Returns
        -------
        Store
            The `Store` instance matching the criteria.

        Raises
        ------
        ValueError
            If neither store_id nor name is provided.
        StoreNotFoundError
            If no store is found.

        Notes
        -----
        - If both are provided, `store_id` takes precedence.
        """
        if store_id is not None:
            result = self._get_store_by_id(store_id=store_id)
        elif name is not None:
            result = self._get_store_by_name(name=name)
        else:
            raise ValueError("Either store ID or name must be provided.")

        if result is None:
            raise (
                StoreNotFoundError(store_id=store_id)
                if store_id is not None
                else StoreNotFoundError(name=name)
            )

        return result

    def get_all_stores(self) -> list[Store]:
        """
        Retrieve all stores from the database.

        Returns
        -------
        list[Store]
            A list of all `Store` instances.
        """
        return self.db_session.query(Store).all()

    def update_store(
        self,
        store_id: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Store:
        """
        Update an existing store's fields.

        Parameters
        ----------
        store_id : int
            The unique ID of the store to update.
        name : Optional[str]
            New name. Default is None (no change).
        address : Optional[str]
            New address. Default is None (no change).
        longitude : Optional[float]
            New longitude. Default is None (no change).
        latitude : Optional[float]
            New latitude. Default is None (no change).
        phone : Optional[str]
            New phone number. Default is None (no change).
        website : Optional[str]
            New website. Default is None (no change).
        description : Optional[str]
            New description. Default is None (no change).

        Returns
        -------
        Store
            The updated `Store` instance.

        Raises
        ------
        StoreNotFoundError
            If no store exists with `store_id`.
        StoreExistsError
            If updating the name conflicts with an existing store.
        """
        store = self._get_store_by_id(store_id)
        if store is None:
            raise StoreNotFoundError(store_id=store_id)

        if name is not None:
            store.name = name
        if address is not None:
            store.address = address
        if longitude is not None:
            store.longitude = longitude
        if latitude is not None:
            store.latitude = latitude
        if phone is not None:
            store.phone = phone
        if website is not None:
            store.website = website
        if description is not None:
            store.description = description

        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise StoreExistsError(name if name is not None else store.name)

        return store

    def delete_store(self, store_id: int) -> None:
        """
        Delete a store from the database by its unique ID.

        Parameters
        ----------
        store_id : int
            The unique ID of the store to delete.

        Raises
        ------
        StoreNotFoundError
            If no store is found with the given ID.
        """
        store = self._get_store_by_id(store_id)
        if store is None:
            raise StoreNotFoundError(store_id=store_id)
        self.db_session.delete(store)
        self.db_session.commit()

    def _get_store_by_id(self, store_id: int) -> Optional[Store]:
        """
        Retrieve a store from the database by its unique ID.

        Parameters
        ----------
        store_id : int
            The unique ID of the store to retrieve.

        Returns
        -------
        Optional[Store]
            The `Store` instance if found, otherwise `None`.

        Notes
        -----
        No business logic should be placed here.
        """
        return self.db_session.query(Store).filter_by(id=store_id).first()

    def _get_store_by_name(self, name: str) -> Optional[Store]:
        """
        Retrieve a store from the database by its name.

        Parameters
        ----------
        name : str
            The name of the store to retrieve.

        Returns
        -------
        Optional[Store]
            The `Store` instance if found, otherwise `None`.

        Notes
        -----
        No business logic should be placed here.
        """
        return self.db_session.query(Store).filter_by(name=name).first()
