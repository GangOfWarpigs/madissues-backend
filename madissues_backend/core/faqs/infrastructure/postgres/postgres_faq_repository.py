from typing import Optional

from sqlalchemy.orm import Session

from madissues_backend.core.faqs.application.ports.faq_repository import FaqRepository
from madissues_backend.core.faqs.domain.faq import Faq
from madissues_backend.core.faqs.domain.postgres.faq_model import PostgresFaq
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class PostgresFaqRepository(FaqRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, faq: Faq) -> Faq:
        self._session.add(PostgresFaq.from_entity(faq))
        self._session.commit()
        return faq

    def save(self, faq: Faq) -> Faq:
        self._session.merge(PostgresFaq.from_entity(faq))
        self._session.commit()
        return faq

    def remove(self, faq_id: GenericUUID):
        faq = self._session.query(PostgresFaq).filter_by(id=faq_id).one()
        self._session.delete(faq)
        self._session.commit()

    def get_by_id(self, faq_id: GenericUUID) -> Optional[Faq]:
        faq = self._session.query(PostgresFaq).filter_by(id=faq_id).one_or_none()
        return faq.to_entity() if faq else None

    def get_all_organization_faqs(self, org_id):
        faqs = self._session.query(PostgresFaq).filter_by(organization_id=org_id).all()
        return [faq.to_entity() for faq in faqs]


