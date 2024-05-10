from abc import ABC, abstractmethod

from madissues_backend.core.organizations.domain.read_models.OrganizationReadModel import OrganizationReadModel


class OrganizationQueryRepository(ABC):
    @abstractmethod
    def get_all_by_owner(self, owner_id: str) -> list[OrganizationReadModel]:
        ...
    @abstractmethod
    def get_by_id(self, id: str) -> OrganizationReadModel:
        ...
