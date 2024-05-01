from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class IssueCreatedPayload(BaseModel):
    user_id: str
    email: str


class IssueCreated(DomainEvent[IssueCreatedPayload]):
    name: str = "@owner/email_updated"
