from pydantic import BaseModel

from madissues_backend.core.issues.domain.events.issue_deleted import IssueDeleted, IssueDeletedPayload
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class DeleteIssueRequest(BaseModel):
    issue_id: str  # GenericUUID of the issue to delete
    user_id: str  # GenericUUID of the user attempting to delete


class DeleteIssueResponse(BaseModel):
    id: str  # ID of the deleted issue


@students_only
class DeleteIssueCommand(Command[DeleteIssueRequest, DeleteIssueResponse]):
    def __init__(self, authentication_service: AuthenticationService, issue_repository: IssueRepository):
        self.authentication_service = authentication_service
        self.issue_repository = issue_repository

    def execute(self, request: DeleteIssueRequest) -> Response[DeleteIssueResponse]:
        issue = self.issue_repository.get_by_id(GenericUUID(request.issue_id))
        if not issue:
            return Response.fail(code=404, message="Issue not found")

        # Check if the user requesting the deletion is the author or a site admin
        if (issue.student_id != GenericUUID(request.user_id) and
                not self.authentication_service.is_site_admin()):
            return Response.fail(code=401, message="Unauthorized. You are not the author of the issue or a site admin")

        self.issue_repository.remove(issue.id)

        issue.register_event(
            IssueDeleted(
                payload=IssueDeletedPayload(
                    issue_id=str(issue.id),
                    student_id=str(issue.student_id),
                    organization_id=str(issue.organization_id)
                )
            )
        )

        return Response.ok(
            DeleteIssueResponse(id=str(issue.id))
        )
