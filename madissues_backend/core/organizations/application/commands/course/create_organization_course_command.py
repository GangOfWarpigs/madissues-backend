from pydantic import BaseModel, Field, ValidationError

from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse


class CreateOrganizationCourseRequest(BaseModel):
    organization_id: str
    name: str
    code: str
    year: int
    icon: str
    primary_color: str
    secondary_color: str


class CreateOrganizationCourseResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    code: str
    year: int
    icon: str
    primary_color: str
    secondary_color: str


@owners_only
class CreateOrganizationCourseCommand(Command[CreateOrganizationCourseRequest, CreateOrganizationCourseResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.repository = repository
        self.event_bus = event_bus

    def execute(self, request: CreateOrganizationCourseRequest) -> Response[CreateOrganizationCourseResponse]:
        try:
            organization = self.repository.get_by_id(GenericUUID(request.organization_id))
            assert organization is not None
        except (ValidationError, ValueError, AttributeError):
            return Response.fail(message="Invalid organization ID")

        # Check if the requestor is the owner of the organization
        if not self.authentication_service.is_owner_of(str(organization.id)):
            return Response.fail(message="You are not the owner of the organization")

        course = OrganizationCourse(
            id=GenericUUID.next_id(),
            name=request.name,
            code=request.code,
            year=request.year,
            icon=request.icon,
            primary_color=request.primary_color,
            secondary_color=request.secondary_color
        )
        # Add the course to the organization
        try:
            organization.add_course(course)
        except ValueError as e:
            return Response.fail(message=str(e)) # Course already exists

        self.event_bus.notify_all(organization.collect_events())

        # Save the organization
        self.repository.save(organization)

        return Response.ok(CreateOrganizationCourseResponse(
            id=str(course.id),
            organization_id=str(organization.id),
            name=course.name,
            code=course.code,
            year=course.year,
            icon=course.icon,
            primary_color=course.primary_color,
            secondary_color=course.secondary_color
        ))
