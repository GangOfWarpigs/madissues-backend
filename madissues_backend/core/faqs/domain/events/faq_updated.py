from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class FaqUpdatedPayload(BaseModel):
    id: str
    question: str
    answer: str
    organization_id: str


class FaqUpdated(DomainEvent[FaqUpdatedPayload]):
    name: str = "@faq/faq_updated"
