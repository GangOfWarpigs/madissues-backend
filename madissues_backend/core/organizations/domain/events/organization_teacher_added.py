from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationTeacherAddedPayload(BaseModel):
    first_name: str
    last_name: str
    email: str | None
    office_link: str | None
    courses: list[GenericUUID]


class OrganizationTeacherAdded(DomainEvent[OrganizationTeacherAddedPayload]):
    name: str = "@organization/teacher_added"
