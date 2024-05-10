from pydantic import BaseModel
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse

class OrganizationCourseReadModel(BaseModel):
    id: str
    name: str
    code: str
    icon: str
    primary_color: str
    secondary_color: str

    @staticmethod
    def of(course: OrganizationCourse):
        return OrganizationCourseReadModel(
            id=str(course.id),
            name=course.name,
            code=course.code,
            icon=course.icon,
            primary_color=course.primary_color,
            secondary_color=course.secondary_color
        )
