from pydantic import BaseModel

from madissues_backend.core.issues.application.ports.issue_query_repository import IssueQueryRepository
from madissues_backend.core.issues.domain.read_models.issue_read_model import IssueReadModel
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.query import Query
from madissues_backend.core.shared.domain.response import Response


class FindIssueDetailedQueryParam(BaseModel):
    issue_id: str


class GetDetailedIssueQuery(Query[FindIssueDetailedQueryParam, IssueReadModel]):
    def __init__(self, authentication_service: AuthenticationService, query_repository: IssueQueryRepository):
        self.authentication_service = authentication_service
        self.query_repository = query_repository

    def execute(self, params: FindIssueDetailedQueryParam | None = None) -> Response[IssueReadModel]:
        if not self.authentication_service.is_authenticated():
            return Response.fail(code=403, message="User must be authenticated")
        if params is not None:
            return Response.ok(self.query_repository.get_by_id(params.issue_id))
        return Response.fail(message="you must send an id")
