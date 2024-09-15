from abc import ABC, abstractmethod

from madissues_backend.core.faqs.domain.faq import Faq
from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class FaqRepository(GenericRepository[GenericUUID, Faq], ABC):
    @abstractmethod
    def add(self, organization: Faq):
        pass

    @abstractmethod
    def remove(self, organization_id: GenericUUID):
        pass

    @abstractmethod
    def get_by_id(self, organization_id: GenericUUID) -> Faq:
        pass

    @abstractmethod
    def save(self, entity: Faq):
        pass

    @abstractmethod
    def get_all_organization_faqs(self, org_id):
        pass
