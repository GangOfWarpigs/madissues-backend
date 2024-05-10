from madissues_backend.core.owners.application.ports.owner_query_repository import OwnerQueryRepository
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.owners.domain.read_models.owner_read_model import OwnerReadModel
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockOwnerQueryRepository(OwnerQueryRepository):
    def __init__(self, db: EntityTable):
        self.db = db

    def get_owner_profile(self, id: str) -> OwnerReadModel:
        owner: Owner = self.db.tables["owners"][GenericUUID(id)]
        return OwnerReadModel.of(owner)
