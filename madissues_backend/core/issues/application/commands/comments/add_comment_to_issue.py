from datetime import datetime

from pydantic import BaseModel

from madissues_backend.core.issues.application.ports.issue_comment_repository import IssueCommentRepository
from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import students_only, Command
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class AddCommentToIssueRequest(BaseModel):
    issue_id: str  # GenericUUID of the issue
    content: str  # Content of the comment
    response_to_id: str | None = None  # Optional GenericUUID of the comment being responded to


class AddCommentToIssueResponse(BaseModel):
    id: str
    issue_id: str
    author_id: str
    content: str
    date_time: str
    response_to_id: str | None


@students_only
class AddCommentToIssueCommand(Command[AddCommentToIssueRequest, AddCommentToIssueResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 issue_comment_repository: IssueCommentRepository):
        self.authentication_service = authentication_service
        self.issue_comment_repository = issue_comment_repository

    def execute(self, request: AddCommentToIssueRequest) -> Response[AddCommentToIssueResponse]:
        # Create the new IssueComment object
        new_comment = IssueComment(
            id=GenericUUID.next_id(),
            issue_id=GenericUUID(request.issue_id),
            author=GenericUUID(self.authentication_service.get_user_id()),
            content=request.content,
            date_time=datetime.now(),
            response_to=GenericUUID(request.response_to_id) if request.response_to_id else None,
            likes=[]
        )

        # Add the comment to the repository
        self.issue_comment_repository.add(new_comment)

        # (Optional) You might want to add some domain events here if needed

        # Return the successful response
        return Response.ok(AddCommentToIssueResponse(
            id=str(new_comment.id),
            issue_id=request.issue_id,
            author_id=str(new_comment.author),
            content=request.content,
            date_time=new_comment.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            response_to_id=request.response_to_id
        ))
