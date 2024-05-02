from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class StudentBannedPayload(BaseModel):
    user_id: str


class StudentBanned(DomainEvent[StudentBannedPayload]):
    name: str = "@student/banned"
