from pydantic import BaseModel

from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.organizations.domain.read_models.organization_task_manager_read_model import \
    OrganizationTaskManagerReadModel
from madissues_backend.core.shared.application.query import Query
from madissues_backend.core.shared.domain.response import Response


class GetOrganizationTaskManagerQueryParams(BaseModel):
    organization_id: str


class GetOrganizationTaskManagerQuery(
    Query[GetOrganizationTaskManagerQueryParams, OrganizationTaskManagerReadModel]):
    def __init__(self, query_repository: OrganizationQueryRepository):
        self.query_repository = query_repository

    def execute(self, params: GetOrganizationTaskManagerQueryParams | None = None) -> Response[
        OrganizationTaskManagerReadModel]:
        if params is None:
            return Response.fail(message="You need to pass an id")
        return Response.ok(self.query_repository.get_organization_task_manager(params.organization_id))
