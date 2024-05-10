from pydantic import Field, BaseModel

from madissues_backend.core.organizations.domain.organization_teacher import OrganizationTeacher


class OrganizationTeacherReadModel(BaseModel):
    id: str
    first_name: str  # min 1
    last_name: str  # min 1
    email: str | None  # email valid
    office_link: str | None
    courses: list[str]

    @staticmethod
    def of(teacher: OrganizationTeacher):
        return OrganizationTeacherReadModel(
            id=str(teacher.id),
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            email=teacher.email,
            office_link=teacher.office_link,
            courses=[str(x) for x in teacher.courses]
        )
