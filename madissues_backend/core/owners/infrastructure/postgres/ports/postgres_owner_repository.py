from typing import Optional

from sqlalchemy import exc
from sqlalchemy.orm import Session

from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.owners.domain.postgres.postgres_owner_model import PostgresOwner
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class PostgresOwnerRepository(OwnerRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, owner: Owner):
        owner_model = self._map_to_model(owner)
        self._session.add(owner_model)
        self._session.commit()

    def remove(self, owner_id: GenericUUID):
        try:
            owner_model = self._session.query(PostgresOwner).filter_by(id=owner_id).one()
            self._session.delete(owner_model)
            self._session.commit()
        except exc.NoResultFound:
            raise ValueError("Owner not found with ID: {}".format(owner_id))

    def get_by_id(self, owner_id: GenericUUID) -> Optional[Owner]:
        try:
            owner_model = self._session.query(PostgresOwner).filter_by(id=owner_id).one()
            return self._map_to_entity(owner_model)
        except exc.NoResultFound:
            return None

    def save(self, owner: Owner):
        owner_model = self._map_to_model(owner)
        self._session.merge(owner_model)
        self._session.commit()

    def exists_owner_with_email(self, email: str) -> bool:
        return self._session.query(
            self._session.query(PostgresOwner).filter_by(email=email).exists()
        ).scalar()

    def get_owner_by_email(self, email: str) -> Optional[Owner]:
        try:
            owner_model = self._session.query(PostgresOwner).filter_by(email=email).one()
            return self._map_to_entity(owner_model)
        except exc.NoResultFound:
            return None

    @staticmethod
    def _map_to_model(owner: Owner) -> PostgresOwner:
        return PostgresOwner(
            id=owner.id,
            email=owner.email,
            first_name=owner.first_name,
            last_name=owner.last_name,
            phone_number=owner.phone_number,
            password=owner.password,  # Assume password is already hashed
            token=owner.token
        )

    @staticmethod
    def _map_to_entity(owner_model: PostgresOwner) -> Owner:
        return Owner(
            id=owner_model.id,
            email=owner_model.email,
            first_name=owner_model.first_name,
            last_name=owner_model.last_name,
            phone_number=owner_model.phone_number,
            password=owner_model.password,
            token=owner_model.token
        )
