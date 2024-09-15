from typing import Optional, Dict
from uuid import UUID

from madissues_backend.core.faqs.application.ports.faq_repository import FaqRepository
from madissues_backend.core.faqs.domain.faq import Faq
from madissues_backend.core.shared.application.mock_repository import GenericMockRepository, EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockFaqRepository(FaqRepository, GenericMockRepository[UUID, Faq]):
    def __init__(self, entity_table: EntityTable):
        super().__init__(entity_table)
        self._faqs: Dict[UUID, Faq] = self.entity_table.tables["faqs"]

    def add(self, faq: Faq) -> Faq:
        self._faqs[faq.id] = faq
        return faq

    def save(self, faq: Faq) -> Faq:
        if faq.id not in self._faqs:
            raise ValueError(f"Faq with id {faq.id} does not exist")
        self._faqs[faq.id] = faq
        return faq

    def remove(self, faq_id: GenericUUID):
        if faq_id not in self._faqs:
            raise ValueError(f"Faq with id {faq_id} does not exist")
        del self._faqs[faq_id]

    def get_by_id(self, faq_id: GenericUUID) -> Optional[Faq]:
        return self._faqs.get(faq_id)

    def get_all_organization_faqs(self, org_id):
        return [faq for faq in self._faqs.values() if faq.organization_id == org_id]
