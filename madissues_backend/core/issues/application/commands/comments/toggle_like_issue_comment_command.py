from pydantic import BaseModel
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.issues.application.ports.issue_comment_repository import IssueCommentRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class LikeCommentRequest(BaseModel):
    comment_id: str  # GenericUUID of the comment to like
    user_id: str  # GenericUUID of the user liking the comment


class LikeCommentResponse(BaseModel):
    id: str  # ID of the liked comment
    likes_count: int  # Total number of likes after the operation


@students_only
class ToggleLikeIssueCommentCommand(Command[LikeCommentRequest, LikeCommentResponse]):
    def __init__(self, authentication_service: AuthenticationService, issue_comment_repository: IssueCommentRepository):
        self.authentication_service = authentication_service
        self.issue_comment_repository = issue_comment_repository

    def execute(self, request: LikeCommentRequest) -> Response[LikeCommentResponse]:

        comment = self.issue_comment_repository.get_by_id(GenericUUID(request.comment_id))
        if not comment:
            return Response.fail(code=404, message="Comment not found")

        user_id = GenericUUID(request.user_id)
        # Check if the user has already liked the comment -> unlike it
        if user_id in comment.likes:
            comment.likes.remove(user_id)
            self.issue_comment_repository.save(comment)
            return Response.ok(LikeCommentResponse(id=str(comment.id), likes_count=len(comment.likes)))
        else:
            comment.likes.append(user_id)
            self.issue_comment_repository.save(comment)
            return Response.ok(LikeCommentResponse(id=str(comment.id), likes_count=len(comment.likes)))
