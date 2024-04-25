from typing import Dict, Union

from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
# Importa los repositorios que deseas incluir en el diccionario
from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.owners.infrastructure.mocks.in_memory_owner_repository import InMemoryOwnerRepository

# Define el tipo para los repositorios
RepositoryType = Union[OwnerRepository, OrganizationRepository]

# Define el diccionario general que contendrá los repositorios
repository_table: Dict[str, RepositoryType] = {
    'owners': InMemoryOwnerRepository(),
    'organizations': MockOrganizationRepository(),
}
