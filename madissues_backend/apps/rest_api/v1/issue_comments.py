from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, issue_comment_repository, \
    issue_comment_query_repository
from madissues_backend.core.issues.application.commands.comments.add_comment_to_issue import AddCommentToIssueRequest, \
    AddCommentToIssueResponse, AddCommentToIssueCommand
from madissues_backend.core.issues.application.commands.comments.change_issue_comment_command import \
    ChangeIssueCommentCommand, ChangeCommentResponse, ChangeCommentRequest
from madissues_backend.core.issues.application.commands.comments.delete_issue_comment_command import \
    DeleteCommentRequest, DeleteCommentResponse, DeleteCommentCommand
from madissues_backend.core.issues.application.commands.comments.toggle_like_issue_comment_command import \
    ToggleLikeIssueCommentCommand, ToggleLikeCommentRequest, ToggleLikeCommentResponse
from madissues_backend.core.issues.application.queries.comments.find_all_comments_of_issue_query import \
    FindAllCommentsOfIssueQuery, FindAllCommentsOfIssueQueryParams
from madissues_backend.core.issues.domain.read_models.issue_comment_read_model import IssueCommentReadModel
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/issues/{id}/comments/", tags=["issues"])
def add_issue_comment(request: AddCommentToIssueRequest,
                      token: Annotated[str, Header()]) -> Response[AddCommentToIssueResponse]:
    authorization = authorization_service(token)
    command = AddCommentToIssueCommand(authentication_service=authorization,
                                       issue_comment_repository=issue_comment_repository)
    return command.run(request)


@router.delete("/issues/{id}/comments/", tags=["issues"])
def delete_issue_comment(request: DeleteCommentRequest,
                         token: Annotated[str, Header()]) -> Response[DeleteCommentResponse]:
    authorization = authorization_service(token)
    command = DeleteCommentCommand(authentication_service=authorization,
                                   issue_comment_repository=issue_comment_repository)
    return command.run(request)


@router.put("/issues/{id}/comments/", tags=["issues"])
def change_issue_comment(request: ChangeCommentRequest,
                         token: Annotated[str, Header()]) -> Response[ChangeCommentResponse]:
    authorization = authorization_service(token)
    command = ChangeIssueCommentCommand(authentication_service=authorization,
                                        issue_comment_repository=issue_comment_repository)
    return command.run(request)


@router.put("/issues/{id}/toggle_like", tags=["issues"])
def toggle_like_issue_comment(request: ToggleLikeCommentRequest,
                              token: Annotated[str, Header()]) -> Response[ToggleLikeCommentResponse]:
    authorization = authorization_service(token)
    command = ToggleLikeIssueCommentCommand(authentication_service=authorization,
                                            issue_comment_repository=issue_comment_repository)
    return command.run(request)


@router.get("issues/{id}/issue_comments/", tags=["issue_comments"])
def get_all_issue_comments_for_issue(id: str, token: Annotated[str, Header()]) -> Response[list[IssueCommentReadModel]]:
    authorization = authorization_service(token)
    query = FindAllCommentsOfIssueQuery(authentication_service=authorization, 
                                        query_repository=issue_comment_query_repository)
    return query.run(
        FindAllCommentsOfIssueQueryParams(
            issue_id=id)
    )
