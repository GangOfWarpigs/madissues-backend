from typing import Annotated

from pydantic import Field

from madissues_backend.core.organizations.domain.events.organization_teacher_added import OrganizationTeacherAdded, \
    OrganizationTeacherAddedPayload
from madissues_backend.core.organizations.domain.events.organization_teacher_deleted import OrganizationTeacherDeleted, \
    OrganizationTeacherDeletedPayload
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse
from madissues_backend.core.organizations.domain.organization_degree import OrganizationDegree
from madissues_backend.core.organizations.domain.organization_teacher import OrganizationTeacher
from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.storage_service import StorageService
from madissues_backend.core.shared.domain.value_objects import GenericUUID

Name = Annotated[str, Field(min_length=1, max_length=280)]
Description = Annotated[str, Field(min_length=1, max_length=280)]
LinkToImage = Annotated[str, Field(min_length=1, pattern=r'^.*\.(png|jpe?g)$')]
HexadecimalColor = Annotated[str, Field(min_length=1, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')]
ContactInfo = Annotated[str, Field(min_length=1, max_length=80)]


class Organization(AggregateRoot[GenericUUID]):
    owner_id: GenericUUID
    name: Name
    logo: LinkToImage | None = Field(init=False, default=None)
    description: Description
    contact_info: ContactInfo
    primary_color: HexadecimalColor
    secondary_color: HexadecimalColor
    teachers: list[OrganizationTeacher] = Field(default=[], init=False)
    courses: list[OrganizationCourse] = Field(default=[], init=False)
    degrees: list[OrganizationDegree] = Field(default=[], init=False)

    def upload_logo(self, image, storage: StorageService):
        logo = storage.upload_b64_image(image)
        self.validate_field("logo", logo)
        self.logo = logo

    def add_teacher(self, teacher: OrganizationTeacher):
        # Check if the teacher is already in the organization with index
        if teacher in self.teachers:
            raise ValueError("Teacher already exists")
        self.teachers.append(teacher)
        self.register_event(
            OrganizationTeacherAdded(
                payload=OrganizationTeacherAddedPayload(
                    first_name=teacher.first_name,
                    last_name=teacher.last_name,
                    email=teacher.email,
                    office_link=teacher.office_link,
                    courses=[course_id for course_id in teacher.courses]
                )
            )
        )

    def get_teacher_by_id(self, teacher_id: GenericUUID) -> OrganizationTeacher | None:
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    def delete_teacher(self, teacher_id: GenericUUID):
        teacher = self.get_teacher_by_id(teacher_id)
        if teacher is None:
            raise ValueError("Teacher not found")
        self.teachers.remove(teacher)
        self.register_event(
            OrganizationTeacherDeleted(
                payload=OrganizationTeacherDeletedPayload(
                    teacher_id=str(teacher.id)
                )
            )
        )
