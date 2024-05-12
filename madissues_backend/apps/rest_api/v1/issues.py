from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, issue_repository, storage_service, \
    event_bus
from madissues_backend.core.issues.application.commands.issues.create_issue_command import CreateIssueRequest, \
    CreateIssueResponse, CreateIssueCommand
from madissues_backend.core.issues.application.queries.issues.get_detailed_issue_query import GetDetailedIssueQuery, \
    FindIssueDetailedQueryParam
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/issues/", tags=["issues"])
def create_issues(request: CreateIssueRequest,
                  token: Annotated[str, Header()]) -> Response[CreateIssueResponse]:
    authorization = authorization_service(token)
    command = CreateIssueCommand(authorization, issue_repository, storage_service, event_bus)
    return command.run(request)


@router.get("/issues/{issue_id}", tags=["issues"])
def get_issue(issue_id: str, token: Annotated[str, Header()]) -> Response:
    authorization = authorization_service(token)
    command = GetDetailedIssueQuery(authorization, issue_repository)
    return command.run(
        FindIssueDetailedQueryParam(issue_id=issue_id)
    )
