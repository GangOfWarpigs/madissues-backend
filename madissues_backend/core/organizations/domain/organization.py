from typing import Annotated

from pydantic import Field

from madissues_backend.core.organizations.domain.events.organization_course_added import OrganizationCourseAdded, \
    OrganizationCourseAddedPayload
from madissues_backend.core.organizations.domain.events.organization_course_deleted import OrganizationCourseDeleted, \
    OrganizationCourseDeletedPayload
from madissues_backend.core.organizations.domain.events.organization_degree_added import OrganizationDegreeAdded, \
    OrganizationDegreeAddedPayload
from madissues_backend.core.organizations.domain.events.organization_degree_deleted import \
    OrganizationDegreeDeletedPayload, OrganizationDegreeDeleted
from madissues_backend.core.organizations.domain.events.organization_teacher_added import OrganizationTeacherAdded, \
    OrganizationTeacherAddedPayload
from madissues_backend.core.organizations.domain.events.organization_teacher_deleted import OrganizationTeacherDeleted, \
    OrganizationTeacherDeletedPayload
from madissues_backend.core.organizations.domain.events.organization_teacher_updated import OrganizationTeacherUpdated, \
    OrganizationTeacherUpdatedPayload
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
        logo = storage.upload_b64_image(image, final_name=str(GenericUUID.next_id()))
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

    def update_teacher(self, updated_teacher: OrganizationTeacher) -> bool:
        for index, teacher in enumerate(self.teachers):
            if teacher.id == updated_teacher.id:
                self.teachers[index] = updated_teacher
                break
        else:
            return False

        self.register_event(
            OrganizationTeacherUpdated(
                payload=OrganizationTeacherUpdatedPayload(
                    teacher_id=str(updated_teacher.id),
                    first_name=updated_teacher.first_name,
                    last_name=updated_teacher.last_name,
                    email=updated_teacher.email,
                    office_link=updated_teacher.office_link,
                    courses=[course_id for course_id in updated_teacher.courses]
                )
            )
        )
        return True

    def get_course_by_id(self, course_id: GenericUUID) -> OrganizationCourse | None:
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def add_course(self, course: OrganizationCourse):
        # Check if the course is already in the organization with index
        if course in self.courses:
            raise ValueError("Course already exists")
        self.courses.append(course)
        self.register_event(
            OrganizationCourseAdded(
                payload=OrganizationCourseAddedPayload(
                    id=str(course.id),
                    organization_id=str(self.id),
                    name=course.name,
                    code=course.code,
                    icon=course.icon,
                    primary_color=course.primary_color,
                    secondary_color=course.secondary_color
                )
            )
        )

    def delete_course(self, course_id: GenericUUID):
        course = self.get_course_by_id(course_id)
        if course is None:
            raise ValueError("Course not found")
        self.courses.remove(course)
        self.register_event(
            OrganizationCourseDeleted(
                payload=OrganizationCourseDeletedPayload(
                    id=str(course.id),
                    organization_id=str(self.id),
                )
            )
        )

    def update_course(self, updated_course: OrganizationCourse) -> bool:
        for index, course in enumerate(self.courses):
            if course.id == updated_course.id:
                self.courses[index] = updated_course
                break
        else:
            return False

        self.register_event(
            OrganizationCourseAdded(
                payload=OrganizationCourseAddedPayload(
                    id=str(updated_course.id),
                    organization_id=str(self.id),
                    name=updated_course.name,
                    code=updated_course.code,
                    icon=updated_course.icon,
                    primary_color=updated_course.primary_color,
                    secondary_color=updated_course.secondary_color
                )
            )
        )
        return True

    def get_degree_by_id(self, degree_id: GenericUUID) -> OrganizationDegree | None:
        for degree in self.degrees:
            if degree.id == degree_id:
                return degree
        return None

    def add_degree(self, degree: OrganizationDegree):
        # Check if the degree is already in the organization with index
        if degree in self.degrees:
            raise ValueError("Degree already exists")
        self.degrees.append(degree)
        # Register event
        self.register_event(
            OrganizationDegreeAdded(
                payload=OrganizationDegreeAddedPayload(
                    id=str(degree.id),
                    organization_id=str(self.id),
                    name=degree.name
                )
            )
        )

    def delete_degree(self, degree_id: GenericUUID):
        degree = self.get_degree_by_id(degree_id)
        if degree is None:
            raise ValueError("Degree not found")
        self.degrees.remove(degree)
        self.register_event(
            OrganizationDegreeDeleted(
                payload=OrganizationDegreeDeletedPayload(
                    id=str(degree.id),
                    organization_id=str(self.id),
                )
            )
        )