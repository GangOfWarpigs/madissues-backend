from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.organizations.domain.read_models.organization_degree_read_model import \
    OrganizationDegreeReadModel
from madissues_backend.core.organizations.domain.read_models.organization_read_model import OrganizationReadModel
from madissues_backend.core.organizations.domain.read_models.organization_teacher_read_model import \
    OrganizationTeacherReadModel
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import owners_only
from madissues_backend.core.shared.application.query import Query, QueryParams, QueryResult
from madissues_backend.core.shared.domain.response import Response


class GetOrganizationDegreesQuery(Query[str, list[OrganizationDegreeReadModel]]):
    def __init__(self, authentication_service: AuthenticationService, query_repository: OrganizationQueryRepository):
        self.authentication_service = authentication_service
        self.query_repository = query_repository

    def execute(self, params: str | None = None) -> Response[list[OrganizationDegreeReadModel]]:
        if not self.authentication_service.is_owner():
            return Response.fail(code=403, message="User must be a owner")

        if params is None:
            return Response.fail(message="You need to pass an id")
        return Response.ok(self.query_repository.get_all_teachers_degrees_organization(params))
