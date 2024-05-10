from pydantic import BaseModel, ValidationError

from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.organizations.domain.organization_teacher import OrganizationTeacher
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class UpdateOrganizationTeacherRequest(BaseModel):
    teacher_id: str
    organization_id: str
    first_name: str
    last_name: str
    email: str
    office_link: str
    courses: list[str] = []


class UpdateOrganizationTeacherResponse(BaseModel):
    teacher_id: str
    organization_id: str
    first_name: str
    last_name: str
    email: str
    office_link: str
    courses: list[str]


@owners_only
class UpdateOrganizationTeacherCommand(Command[UpdateOrganizationTeacherRequest, UpdateOrganizationTeacherResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.repository = repository
        self.event_bus = event_bus

    def execute(self, request: UpdateOrganizationTeacherRequest) -> Response[UpdateOrganizationTeacherResponse]:
        try:
            organization = self.repository.get_by_id(GenericUUID(request.organization_id))
            assert organization is not None
        except (ValidationError, ValueError, AttributeError):
            return Response.fail(message="Invalid organization ID")

        # Check if the requestor is the owner of the organization
        if not self.authentication_service.is_owner_of(str(organization.id)):
            return Response.fail(message="You are not the owner of the organization")

        # Find the teacher in the organization
        try:
            teacher_id = GenericUUID(request.teacher_id)
        except (ValidationError, ValueError, AttributeError):
            return Response.fail(message="Invalid teacher ID")

        teacher = organization.get_teacher_by_id(teacher_id)
        if not teacher:
            return Response.fail(message="Teacher not found in the organization")

        # Create new teacher object
        updated_teacher = OrganizationTeacher(
            id=teacher.id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            office_link=request.office_link,
            courses=[GenericUUID(course_id) for course_id in request.courses]
        )

        # Update the teacher in the organization
        success = organization.update_teacher(updated_teacher)
        if not success:
            return Response.fail(message="Teacher not found in the organization")
        self.event_bus.notify_all(organization.collect_events())

        # Save the organization
        self.repository.save(organization)

        return Response.ok(UpdateOrganizationTeacherResponse(
            teacher_id=str(teacher_id),
            organization_id=str(organization.id),
            first_name=updated_teacher.first_name,
            last_name=updated_teacher.last_name,
            email=str(updated_teacher.email),
            office_link=str(updated_teacher.office_link),
            courses=[str(course_id) for course_id in updated_teacher.courses]
        ))
