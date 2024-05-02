from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class StudentRoleChangedPayload(BaseModel):
    user_id: str
    admin: bool
    council_member: bool


class StudentRoleChanged(DomainEvent[StudentRoleChangedPayload]):
    name: str = "@student/role_changed"
