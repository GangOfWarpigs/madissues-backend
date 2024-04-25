from abc import ABC, abstractmethod
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationRepository(GenericRepository[GenericUUID, Organization], ABC):
    @abstractmethod
    def exists_with_name(self, name : str) -> bool:
        pass

    @abstractmethod
    def get_by_contact_info(self, contact_info: str) -> Organization | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Organization | None:
        pass

    @abstractmethod
    def add(self, organization: Organization):
        pass

    @abstractmethod
    def remove(self, organization_id: GenericUUID):
        pass

    @abstractmethod
    def get_by_id(self, organization_id: GenericUUID) -> Organization:
        pass

    @abstractmethod
    def save(self, entity: Organization):
        pass

