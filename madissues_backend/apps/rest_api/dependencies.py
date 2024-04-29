from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_password_hasher import MockPasswordHasher
from madissues_backend.core.shared.infrastructure.mocks.mock_token_generator import MockTokenGenerator

database = EntityTable()
owner_repository = MockOwnerRepository(database)
password_hasher = MockPasswordHasher()
token_generator = MockTokenGenerator()