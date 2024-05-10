from typing import Annotated

from pydantic import Field, BaseModel

from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse
from madissues_backend.core.shared.domain.value_objects import GenericUUID, LinkToImage

class OrganizationCourseReadModel(BaseModel):
    id: str
    name: str
    code: str
    icon: str
    primary_color: str
    secondary_color: str

    @staticmethod
    def of(course : OrganizationCourse):
        return OrganizationCourseReadModel(
            id=str(course.id),
            name=course.name,
            code=course.code,
            icon=course.icon,
            primary_color=course.primary_color,
            secondary_color=course.secondary_color
        )
