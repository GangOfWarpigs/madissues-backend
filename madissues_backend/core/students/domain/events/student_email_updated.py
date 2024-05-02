from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class StudentEmailUpdatedPayload(BaseModel):
    user_id: str
    email: str


class StudentEmailUpdated(DomainEvent[StudentEmailUpdatedPayload]):
    name: str = "@student/email_updated"
