from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class StudentDeletedPayload(BaseModel):
    deletion_requestor_id: str
    user_being_deleted_id: str


class StudentDeleted(DomainEvent[StudentDeletedPayload]):
    name: str = "@student/deleted"
