from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_query_repository import \
    MockOrganizationQueryRepository
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_query_repository import MockOwnerQueryRepository
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.local_storage_service import LocalStorageService
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.mocks.mock_storage_service import MockStorageService
from madissues_backend.core.shared.infrastructure.openssl.sha256_password_hasher import SHA256PasswordHasher
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator
from madissues_backend.core.students.infrastructure.mocks.mock_student_query_repository import \
    MockStudentQueryRepository
from madissues_backend.core.students.infrastructure.mocks.mock_student_repository import MockStudentRepository
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_repository import \
    MockTaskManagerRepository
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_service import MockTaskManagerFactory

database = EntityTable()
database.load_snapshot("with_organization_created")

# utilities
password_hasher = SHA256PasswordHasher()
token_generator = UUIDTokenGenerator()
event_bus = MockEventBus()
task_manager_factory = MockTaskManagerFactory()

# services
storage_service = MockStorageService()
authorization_service = create_mock_authentication_service(database)

# repositories
owner_repository = MockOwnerRepository(database)
organization_repository = MockOrganizationRepository(database)
student_repository = MockStudentRepository(database)
task_manager_repository = MockTaskManagerRepository(database)

# query repositories
organization_query_repository = MockOrganizationQueryRepository(database)
owner_query_repository = MockOwnerQueryRepository(database)
student_query_repository = MockStudentQueryRepository(database)
