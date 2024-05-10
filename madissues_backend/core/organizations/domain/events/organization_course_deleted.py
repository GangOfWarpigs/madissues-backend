from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationCourseDeletedPayload(BaseModel):
    id: str
    organization_id: str


class OrganizationCourseDeleted(DomainEvent[OrganizationCourseDeletedPayload]):
    name: str = "@organization/course_deleted"
