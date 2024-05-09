from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import owners_only
from madissues_backend.core.shared.application.query import Query, QueryParams, QueryResult
from madissues_backend.core.shared.domain.response import Response


class GetOrganizationsOfOwnerQuery(Query):
    def execute(self, params: QueryParams | None = None):
        if not self.authentication_service.is_owner():
            return Response.fail(code=403, message="User must be a student")
        return self.query_repository.get_all_by_owner(self.authentication_service.get_user_id())

    def __init__(self, authentication_service: AuthenticationService, query_repository: OrganizationQueryRepository):
        self.authentication_service = authentication_service
        self.query_repository = query_repository
