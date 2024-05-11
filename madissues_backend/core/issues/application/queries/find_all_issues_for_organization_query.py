from pydantic import BaseModel

from madissues_backend.core.issues.application.ports.issue_query_repository import IssueQueryRepository
from madissues_backend.core.issues.domain.read_models.issue_read_model import IssueReadModel
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.query import Query
from madissues_backend.core.shared.domain.response import Response


class FindAllIssuesQueryParams(BaseModel):
    organization_id: str


class FindAllIssuesQuery(Query[FindAllIssuesQueryParams, list[IssueReadModel]]):
    def __init__(self, authentication_service: AuthenticationService, query_repository: IssueQueryRepository):
        self.authentication_service = authentication_service
        self.query_repository = query_repository

    def execute(self, params: FindAllIssuesQueryParams | None = None) -> Response[list[IssueReadModel]]:
        if not self.authentication_service.is_authenticated():
            return Response.fail(code=403, message="User must be authenticated")
        if params is not None:
            return Response.ok(self.query_repository.get_all_by_organization(params.organization_id))
        return Response.fail(message="you must send an id")
