from pydantic import BaseModel, Field, ValidationError

from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.organizations.domain.organization_teacher import OrganizationTeacher
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class CreateOrganizationTeacherRequest(BaseModel):
    organization_id: str
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str | None = None
    office_link: str | None = None
    courses: list[str] = []


class CreateOrganizationTeacherResponse(BaseModel):
    id: str
    organization_id: str
    first_name: str
    last_name: str
    email: str | None
    office_link: str | None
    courses: list[str]


@owners_only
class CreateOrganizationTeacherCommand(Command[CreateOrganizationTeacherRequest, CreateOrganizationTeacherResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.organization_repository = repository
        self.event_bus = event_bus

    def execute(self, request: CreateOrganizationTeacherRequest) -> Response[CreateOrganizationTeacherResponse]:
        try:
            organization = self.organization_repository.get_by_id(GenericUUID(request.organization_id))
            assert organization is not None
        except (ValidationError, ValueError, AttributeError) as e:
            return Response.fail(message="Invalid organization ID")

        # Check if the requestor is the owner of the organization
        if not self.authentication_service.is_owner_of(str(organization.id)):
            return Response.fail(message="You are not the owner of the organization")

        teacher = OrganizationTeacher(
            id=GenericUUID.next_id(),
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            office_link=request.office_link,
            courses=[GenericUUID(course_id) for course_id in request.courses]
        )
        # Add the teacher to the organization
        try:
            organization.add_teacher(teacher)
        except ValueError as e:
            return Response.fail(message=str(e)) # Teacher already exists

        self.event_bus.notify_all(organization.collect_events())

        # Save the organization
        self.organization_repository.save(organization)

        return Response.ok(CreateOrganizationTeacherResponse(
            id=str(teacher.id),
            organization_id=str(organization.id),
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            email=teacher.email,
            office_link=teacher.office_link,
            courses=[str(course_id) for course_id in teacher.courses]
        ))
