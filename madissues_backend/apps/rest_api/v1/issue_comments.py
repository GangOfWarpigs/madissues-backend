from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, issue_comment_repository
from madissues_backend.core.issues.application.commands.comments.add_comment_to_issue import AddCommentToIssueRequest, \
    AddCommentToIssueResponse, AddCommentToIssueCommand
from madissues_backend.core.issues.application.commands.comments.change_issue_comment_command import \
    ChangeIssueCommentCommand, ChangeCommentResponse, ChangeCommentRequest
from madissues_backend.core.issues.application.commands.comments.delete_issue_comment_command import \
    DeleteCommentRequest, DeleteCommentResponse, DeleteCommentCommand
from madissues_backend.core.issues.application.commands.comments.toggle_like_issue_comment_command import \
    ToggleLikeIssueCommentCommand, ToggleLikeCommentRequest, ToggleLikeCommentResponse
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/issue_comments/", tags=["issue_comments"])
def add_issue_comment(request: AddCommentToIssueRequest,
                      token: Annotated[str, Header()]) -> Response[AddCommentToIssueResponse]:
    authorization = authorization_service(token)
    command = AddCommentToIssueCommand(authentication_service=authorization,
                                       issue_comment_repository=issue_comment_repository)
    return command.run(request)


@router.delete("/issue_comments/", tags=["issue_comments"])
def delete_issue_comment(request: DeleteCommentRequest,
                         token: Annotated[str, Header()]) -> Response[DeleteCommentResponse]:
    authorization = authorization_service(token)
    command = DeleteCommentCommand(authentication_service=authorization,
                                   issue_comment_repository=issue_comment_repository)
    return command.run(request)


@router.put("/issue_comments/", tags=["issue_comments"])
def change_issue_comment(request: ChangeCommentRequest,
                         token: Annotated[str, Header()]) -> Response[ChangeCommentResponse]:
    authorization = authorization_service(token)
    command = ChangeIssueCommentCommand(authentication_service=authorization,
                                        issue_comment_repository=issue_comment_repository)
    return command.run(request)


@router.put("/issue_comments/toggle_like", tags=["issue_comments"])
def toggle_like_issue_comment(request: ToggleLikeCommentRequest,
                              token: Annotated[str, Header()]) -> Response[ToggleLikeCommentResponse]:
    authorization = authorization_service(token)
    command = ToggleLikeIssueCommentCommand(authentication_service=authorization,
                                            issue_comment_repository=issue_comment_repository)
    return command.run(request)


