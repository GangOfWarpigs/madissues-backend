from pydantic import BaseModel, ValidationError

from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse


class UpdateOrganizationCourseRequest(BaseModel):
    course_id: str
    organization_id: str
    name: str
    code: str
    year: int
    icon: str
    primary_color: str
    secondary_color: str


class UpdateOrganizationCourseResponse(BaseModel):
    course_id: str
    organization_id: str
    name: str
    code: str
    year: int
    icon: str
    primary_color: str
    secondary_color: str


@owners_only
class UpdateOrganizationCourseCommand(Command[UpdateOrganizationCourseRequest, UpdateOrganizationCourseResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.repository = repository
        self.event_bus = event_bus

    def execute(self, request: UpdateOrganizationCourseRequest) -> Response[UpdateOrganizationCourseResponse]:
        try:
            organization = self.repository.get_by_id(GenericUUID(request.organization_id))
            assert organization is not None
        except (ValidationError, ValueError, AttributeError):
            return Response.fail(message="Invalid organization ID")

        # Check if the requestor is the owner of the organization
        if not self.authentication_service.is_owner_of(str(organization.id)):
            return Response.fail(message="You are not the owner of the organization")

        # Find the course in the organization
        try:
            course_id = GenericUUID(request.course_id)
        except (ValidationError, ValueError, AttributeError):
            return Response.fail(message="Invalid course ID")

        course = organization.get_course_by_id(course_id)
        if not course:
            return Response.fail(message="Course not found in the organization")

        # Create new course object
        updated_course = OrganizationCourse(
            id=course.id,
            name=request.name,
            code=request.code,
            year=request.year,
            icon=request.icon,
            primary_color=request.primary_color,
            secondary_color=request.secondary_color
        )

        # Update the course in the organization
        success = organization.update_course(updated_course)
        if not success:
            return Response.fail(message="Course not found in the organization")
        self.event_bus.notify_all(organization.collect_events())

        # Save the organization
        self.repository.save(organization)

        return Response.ok(UpdateOrganizationCourseResponse(
            course_id=str(course_id),
            organization_id=str(organization.id),
            name=updated_course.name,
            code=updated_course.code,
            year=updated_course.year,
            icon=updated_course.icon,
            primary_color=updated_course.primary_color,
            secondary_color=updated_course.secondary_color
        ))
