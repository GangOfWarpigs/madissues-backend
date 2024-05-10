from typing import Any

from pydantic import BaseModel

from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.query import Query
from madissues_backend.core.shared.domain.response import Response


class Params(BaseModel):
    id: str


class GetSingleOrganizationQuery(Query[Params, Any]):
    def execute(self, params: Params | None = None):
        if not self.authentication_service.is_owner():
            return Response.fail(code=403, message="User must be a owner")
        if params is not None:
            return self.query_repository.get_by_id(params.id)
        return Response.fail(message="you must send an id")

    def __init__(self, authentication_service: AuthenticationService, query_repository: OrganizationQueryRepository):
        self.authentication_service = authentication_service
        self.query_repository = query_repository
