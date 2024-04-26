from typing import Dict

from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.shared.application.mock_repository import GenericMockRepository, EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockOwnerRepository(OwnerRepository, GenericMockRepository[GenericUUID, Owner]):
    owners: Dict[GenericUUID, Owner]

    def __init__(self, entity_table: EntityTable):
        super().__init__(entity_table)
        self.owners = self.entity_table.tables["owners"]

    def add(self, entity: Owner):
        if self.owners.get(entity.id):
            raise ValueError("Owner already exists")
        self.owners[entity.id] = entity

    def remove(self, owner_id: GenericUUID):
        if not self.owners.get(owner_id):
            raise ValueError("Owner does not exists")
        del self.owners[owner_id]

    def get_by_id(self, owner_id: GenericUUID) -> Owner:
        owner = self.owners.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        return owner

    def save(self, entity: Owner):
        index = self.owners.get(entity.id)
        if index is None:
            raise ValueError("Owner not found")
        self.owners[entity.id] = entity

    def exists_owner_with_email(self, email: str) -> bool:
        for owner in self.owners.values():
            if owner.email == email:
                return True
        return False

    def get_owner_by_email(self, email: str) -> Owner | None:
        for owner in self.owners.values():
            if owner.email == email:
                return owner
        return None

    def get_owned_organizations(self, owner_id: GenericUUID) -> list[Organization]:
        return [org for org in self.entity_table.tables["organizations"].values() if org.owner_id == owner_id]