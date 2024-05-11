from pydantic import BaseModel
from datetime import datetime
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.issues.application.ports.issue_comment_repository import IssueCommentRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class ChangeCommentRequest(BaseModel):
    comment_id: str  # GenericUUID of the comment to change
    user_id: str  # GenericUUID of the user making the change
    new_content: str  # New content for the comment


class ChangeCommentResponse(BaseModel):
    id: str  # ID of the changed comment
    new_content: str  # New content of the comment
    updated_date_time: str  # Updated datetime of the comment


@students_only
class ChangeIssueCommentCommand(Command[ChangeCommentRequest, ChangeCommentResponse]):
    def __init__(self, authentication_service: AuthenticationService, issue_comment_repository: IssueCommentRepository):
        self.authentication_service = authentication_service
        self.issue_comment_repository = issue_comment_repository

    def execute(self, request: ChangeCommentRequest) -> Response[ChangeCommentResponse]:
        comment = self.issue_comment_repository.get_by_id(GenericUUID(request.comment_id))
        if not comment:
            return Response.fail(code=404, message="Comment not found")

        if (comment.author != GenericUUID(request.user_id) and
                not self.authentication_service.is_site_admin()):
            return Response.fail(code=401, message="Unauthorized. You are not the author of the comment")

        # Update the comment
        comment.content = request.new_content
        comment.date_time = datetime.now()
        self.issue_comment_repository.save(comment)

        return Response.ok(ChangeCommentResponse(
            id=str(comment.id),
            new_content=comment.content,
            updated_date_time=comment.date_time.strftime('%Y-%m-%d %H:%M:%S')
        ))
