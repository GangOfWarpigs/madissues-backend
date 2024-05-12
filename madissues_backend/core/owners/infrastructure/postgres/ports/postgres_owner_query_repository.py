from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from madissues_backend.core.owners.domain.read_models.owner_read_model import OwnerReadModel
from madissues_backend.core.owners.domain.postgres.postgres_owner_model import PostgresOwner


class PostgresOwnerQueryRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_owner_profile(self, id: str) -> Optional[OwnerReadModel]:
        try:
            owner = self._session.query(PostgresOwner).filter(PostgresOwner.id == id).one()
            return self._map_to_read_model(owner)
        except NoResultFound:
            return None



    @staticmethod
    def _map_to_read_model(owner: PostgresOwner) -> OwnerReadModel:
        return OwnerReadModel(
            id=str(owner.id),
            email=str(owner.email),
            first_name=str(owner.first_name),
            last_name=str(owner.last_name),
            phone_number=str(owner.phone_number),
        )
