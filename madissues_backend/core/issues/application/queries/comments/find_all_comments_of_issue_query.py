from pydantic import BaseModel

from madissues_backend.core.issues.application.ports.issue_comment_query_repository import IssueCommentQueryRepository
from madissues_backend.core.issues.domain.read_models.issue_comment_read_model import IssueCommentReadModel
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.query import Query
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class FindAllCommentsOfIssueQueryParams(BaseModel):
    issue_id: str


class FindAllCommentsOfIssueQuery(Query[FindAllCommentsOfIssueQueryParams, list[IssueCommentReadModel]]):
    def __init__(self, authentication_service: AuthenticationService, query_repository: IssueCommentQueryRepository):
        self.authentication_service = authentication_service
        self.query_repository = query_repository

    def execute(self, params: FindAllCommentsOfIssueQueryParams | None = None) -> Response[list[IssueCommentReadModel]]:
        if not self.authentication_service.is_authenticated():
            return Response.fail(code=403, message="User must be authenticated")
        if params is not None:
            return Response.ok(
                self.query_repository.get_all_by_issue(
                    GenericUUID(params.issue_id)))
        return Response.fail(message="you must send an id")
