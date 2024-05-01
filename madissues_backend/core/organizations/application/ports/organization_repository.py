from abc import ABC, abstractmethod
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationRepository(GenericRepository[GenericUUID, Organization], ABC):
    @abstractmethod
    def exists_with_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_contact_info(self, contact_info: str) -> Organization | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Organization | None:
        pass
