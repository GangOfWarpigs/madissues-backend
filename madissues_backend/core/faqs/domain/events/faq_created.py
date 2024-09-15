from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class FaqCreatedPayload(BaseModel):
    question: str
    answer: str


class FaqCreated(DomainEvent[FaqCreatedPayload]):
    name: str = "@faq/faq_created"
