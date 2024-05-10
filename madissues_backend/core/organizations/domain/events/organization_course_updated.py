from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationCourseUpdatedPayload(BaseModel):
    id: str
    organization_id: str
    name: str
    code: str
    icon: str
    primary_color: str
    secondary_color: str


class OrganizationCourseUpdated(DomainEvent[OrganizationCourseUpdatedPayload]):
    name: str = "@organization/course_updated"
