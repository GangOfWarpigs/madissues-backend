from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationTeacherUpdatedPayload(BaseModel):
    teacher_id: str
    first_name: str
    last_name: str
    email: str | None
    office_link: str | None
    courses: list[GenericUUID]


class OrganizationTeacherUpdated(DomainEvent[OrganizationTeacherUpdatedPayload]):
    name: str = "@organization/teacher_updated"
