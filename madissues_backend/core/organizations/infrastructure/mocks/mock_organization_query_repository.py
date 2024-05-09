from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable


class MockOrganizationQueryRepository(OrganizationQueryRepository):
    def __init__(self, db: EntityTable) -> object:
        self.db = db

    def get_all_by_owner(self, owner_id: str):
        return self.db.tables["organizations"]
