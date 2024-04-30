from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class OwnerEmailUpdatedPayload(BaseModel):
    user_id: str
    email: str


class OwnerEmailUpdated(DomainEvent[OwnerEmailUpdatedPayload]):
    name : str = "@owner/email_updated"
