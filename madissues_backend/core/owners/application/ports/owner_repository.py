from abc import ABC, abstractmethod

from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.domain.owner import Owner


class OwnerRepository(GenericRepository[GenericUUID, Owner], ABC):
    @abstractmethod
    def exists_owner_with_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def get_owner_by_email(self, email: str) -> Owner | None:
        pass
