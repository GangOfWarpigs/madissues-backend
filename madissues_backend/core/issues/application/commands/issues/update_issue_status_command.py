# Pillar la entidad de issue de la base de datos
# Actualizar el estado del issue
# Persistir en base de datos

from pydantic import BaseModel

from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class UpdateIssueStatusRequest(BaseModel):
    issue_id: str  # GenericUUID of the issue to update
    user_id: str  # GenericUUID of the user attempting to update the issue
    new_status: str  # New status to set (e.g., "In Progress", "Solved")


class UpdateIssueStatusResponse(BaseModel):
    id: str  # ID of the updated issue
    new_status: str  # New status of the issue


@students_only
class UpdateIssueStatusCommand(Command[UpdateIssueStatusRequest, UpdateIssueStatusResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 issue_repository: IssueRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.issue_repository = issue_repository
        self.event_bus = event_bus

    def execute(self, request: UpdateIssueStatusRequest) -> Response[UpdateIssueStatusResponse]:
        issue = self.issue_repository.get_by_id(GenericUUID(request.issue_id))
        if not issue:
            return Response.fail(code=404, message="Issue not found")

        # Verify permissions: User must be either the issue creator, assigned teacher, or a site admin
        if (issue.student_id != GenericUUID(request.user_id)
                and not self.authentication_service.is_site_admin()
                and GenericUUID(request.user_id) not in issue.teachers):
            return Response.fail(code=401, message="Unauthorized to update this issue")

        # Update the status
        issue.update_status(request.new_status)
        self.issue_repository.save(issue)
        self.event_bus.notify_all(issue.collect_events())

        return Response.ok(
            UpdateIssueStatusResponse(
                id=str(issue.id),
                new_status=request.new_status
            )
        )
