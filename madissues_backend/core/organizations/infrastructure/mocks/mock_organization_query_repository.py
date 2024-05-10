from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockOrganizationQueryRepository(OrganizationQueryRepository):

    def __init__(self, db: EntityTable):
        self.db = db

    def get_all_by_owner(self, owner_id: str):
        organizations_map = self.db.tables["organizations"]
        return list(organizations_map.values())

    def get_by_id(self, id: str):
        organization = self.db.tables["organizations"][GenericUUID(id)]
        return organization
