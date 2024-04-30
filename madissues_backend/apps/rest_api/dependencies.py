from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.openssl.sha256_password_hasher import SHA256PasswordHasher
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator

database = EntityTable()
owner_repository = MockOwnerRepository(database)
password_hasher = SHA256PasswordHasher()
token_generator = UUIDTokenGenerator()
authorization_service = create_mock_authentication_service(database)
event_bus = MockEventBus()