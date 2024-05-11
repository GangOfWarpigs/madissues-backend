from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class IssueInfoUpdatedPayload(BaseModel):
    issue_id: str  # GenericUUID
    title: str
    description: str
    details: str
    proofs: list[str]
    teachers: list[str]


class IssueInfoUpdated(DomainEvent[IssueInfoUpdatedPayload]):
    name: str = "@issue/issue_info_updated"
