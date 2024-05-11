from pydantic import BaseModel
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.issues.application.ports.issue_comment_repository import IssueCommentRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class DeleteCommentRequest(BaseModel):
    comment_id: str  # GenericUUID of the comment to delete
    author_id: str  # GenericUUID of the author attempting to delete


class DeleteCommentResponse(BaseModel):
    id: str  # ID of the deleted comment


@students_only
class DeleteCommentCommand(Command[DeleteCommentRequest, DeleteCommentResponse]):
    def __init__(self, authentication_service: AuthenticationService, issue_comment_repository: IssueCommentRepository):
        self.authentication_service = authentication_service
        self.issue_comment_repository = issue_comment_repository

    def execute(self, request: DeleteCommentRequest) -> Response[DeleteCommentResponse]:
        comment = self.issue_comment_repository.get_by_id(GenericUUID(request.comment_id))

        if not comment:
            return Response.fail(code=404, message="Comment not found")

        # Check if the author of the comment or an admin is making the request
        if (comment.author != GenericUUID(self.authentication_service.get_user_id())
                and not self.authentication_service.is_site_admin()):
            return Response.fail(code=401, message="Unauthorized. You are not the author of the comment")

        self.issue_comment_repository.remove(comment.id)

        return Response.ok(DeleteCommentResponse(id=str(comment.id)))
