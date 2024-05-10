from madissues_backend.core.owners.application.ports.owner_query_repository import OwnerQueryRepository
from madissues_backend.core.owners.domain.read_models.owner_read_model import OwnerReadModel
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.query import Query
from madissues_backend.core.shared.domain.response import Response


class GetOwnerProfileQuery(Query[None, OwnerReadModel]):
    def __init__(self, authentication_service: AuthenticationService, query_repository: OwnerQueryRepository):
        self.authentication_service = authentication_service
        self.query_repository = query_repository

    def execute(self, params: None = None) -> Response[OwnerReadModel]:
        if not self.authentication_service.is_owner():
            return Response.fail(code=403, message="User must be a owner")
        return Response.ok(self.query_repository.get_owner_profile(self.authentication_service.get_user_id()))
