from typing import Optional, Dict
from uuid import UUID

from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockOrganizationRepository(OrganizationRepository):
    def __init__(self):
        self._organizations: Dict[UUID, Organization] = {}

    def add(self, organization: Organization) -> Organization:
        self._organizations[organization.id] = organization
        return organization

    def save(self, organization: Organization) -> Organization:
        if organization.id not in self._organizations:
            raise ValueError(f"Organization with id {organization.id} does not exist")
        self._organizations[organization.id] = organization
        return organization

    def remove(self, organization_id: GenericUUID):
        if organization_id not in self._organizations:
            raise ValueError(f"Organization with id {organization_id} does not exist")
        del self._organizations[organization_id]

    def get_by_id(self, organization_id: GenericUUID) -> Optional[Organization]:
        return self._organizations.get(organization_id)

    def get_by_name(self, name: str) -> Optional[Organization]:
        for organization in self._organizations.values():
            if organization.name == name:
                return organization
        return None

    def exists_with_name(self, name: str) -> bool:
        for organization in self._organizations.values():
            if organization.name == name:
                return True
        return False

    def get_by_contact_info(self, contact_info: str) -> Optional[Organization]:
        for organization in self._organizations.values():
            if organization.contact_info == contact_info:
                return organization
        return None
