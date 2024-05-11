from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class IssueStatusUpdatedPayload(BaseModel):
    issue_id: str  # GenericUUID
    new_status: str


class IssueStatusUpdated(DomainEvent[IssueStatusUpdatedPayload]):
    name: str = "@owner/issue_status_updated"
