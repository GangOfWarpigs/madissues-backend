from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationTeacherDeletedPayload(BaseModel):
    teacher_id: str


class OrganizationTeacherDeleted(DomainEvent[OrganizationTeacherDeletedPayload]):
    name: str = "@organization/teacher_deleted"
