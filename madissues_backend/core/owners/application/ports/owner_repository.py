from abc import ABC, abstractmethod

from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.domain.owner import Owner


class OwnerRepository(GenericRepository[GenericUUID, Owner], ABC):
    @abstractmethod
    def exists_owner_with_email(self, email : str) -> bool:
        pass

    @abstractmethod
    def add(self, entity: Owner):
        pass

    @abstractmethod
    def remove(self, user_id: GenericUUID):
        pass

    @abstractmethod
    def get_by_id(self, user_id: GenericUUID) -> Owner:
        pass

    @abstractmethod
    def save(self, entity: Owner):
        pass


