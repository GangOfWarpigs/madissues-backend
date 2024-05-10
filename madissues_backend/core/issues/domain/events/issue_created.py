from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class IssueCreatedPayload(BaseModel):
    title: str
    description: str
    details: str
    proofs: list[str]  # List of image links
    status: str  # Queued, In progress, Solved, Not Solved
    date_time: str
    course: str  # GenericUUID
    teachers: list[str]  # list[GenericUUID]
    student: str  # GenericUUID


class IssueCreated(DomainEvent[IssueCreatedPayload]):
    name: str = "@owner/issue_created"
