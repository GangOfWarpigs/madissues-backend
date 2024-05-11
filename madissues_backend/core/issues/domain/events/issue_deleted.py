from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class IssueDeletedPayload(BaseModel):
    issue_id: str  # GenericUUID
    student_id: str  # GenericUUID
    organization_id: str  # GenericUUID


class IssueDeleted(DomainEvent[IssueDeletedPayload]):
    name: str = "@owner/issue_deleted"
