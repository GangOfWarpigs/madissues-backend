import os

from dotenv import load_dotenv

from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_query_repository import \
    MockIssueCommentQueryRepository
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_repository import MockIssueCommentRepository
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_query_repository import MockIssueQueryRepository
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.issues.infrastructure.postgres.ports.comments.postgres_issue_comment_query_repository import \
    PostgresIssueCommentQueryRepository
from madissues_backend.core.issues.infrastructure.postgres.ports.comments.postgres_issue_comment_repository import \
    PostgresIssueCommentRepository
from madissues_backend.core.issues.infrastructure.postgres.ports.issues.postgres_issue_query_repository import \
    PostgresIssueQueryRepository
from madissues_backend.core.issues.infrastructure.postgres.ports.issues.postgres_issue_repository import \
    PostgresIssueRepository
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_query_repository import \
    MockOrganizationQueryRepository
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.organizations.infrastructure.ports.postgres_organization_query_repository import \
    PostgresOrganizationQueryRepository
from madissues_backend.core.organizations.infrastructure.ports.postgres_organization_repository import \
    PostgresOrganizationRepository
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_query_repository import MockOwnerQueryRepository
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.owners.infrastructure.postgres.ports.postgres_owner_query_repository import \
    PostgresOwnerQueryRepository
from madissues_backend.core.owners.infrastructure.postgres.ports.postgres_owner_repository import \
    PostgresOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.openssl.sha256_password_hasher import SHA256PasswordHasher
from madissues_backend.core.shared.infrastructure.postgres.postgres_manager import PostgresManager
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator
from madissues_backend.core.students.infrastructure.mocks.mock_student_query_repository import \
    MockStudentQueryRepository
from madissues_backend.core.students.infrastructure.mocks.mock_student_repository import MockStudentRepository
from madissues_backend.core.students.infrastructure.postgres.ports.postgres_student_query_repository import \
    PostgresStudentQueryRepository
from madissues_backend.core.students.infrastructure.postgres.ports.postgres_student_repository import \
    PostgresStudentRepository
from madissues_backend.core.task_manager.application.handlers.issue_created_handler import IssueCreatedHandler
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_repository import \
    MockTaskManagerRepository
from madissues_backend.core.task_manager.infrastructure.trello_task_manager_service import TrelloTaskManagerFactory

# Postgres
load_dotenv()

# Obtener valores de las variables de entorno o proporcionar valores predeterminados
POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')

postgres_manager = None
# Only instantiate the PostgresManager if all the environment variables are set
if all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB]):
    postgres_manager = PostgresManager(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db=POSTGRES_DB
    )

# In memory database
database = EntityTable()
database.load_snapshot("with_organization_created")

# utilities
password_hasher = SHA256PasswordHasher()
token_generator = UUIDTokenGenerator()
event_bus = MockEventBus()
task_manager_factory = TrelloTaskManagerFactory()

# services
storage_service = LocalStorageService(media_path="./madissues_backend/media")
authorization_service = create_mock_authentication_service(database)

# mock repositories
# owner_repository = MockOwnerRepository(database)
# organization_repository = MockOrganizationRepository(database)
# student_repository = MockStudentRepository(database)
# task_manager_repository = MockTaskManagerRepository(database)
# issue_repository = MockIssueRepository(database)
# issue_comment_repository = MockIssueCommentRepository(database)
# issue_comment_query_repository = MockIssueCommentQueryRepository(database)

# postgres repositories
if postgres_manager is not None:
    owner_repository = PostgresOwnerRepository(postgres_manager.get_session())
    organization_repository = PostgresOrganizationRepository(postgres_manager.get_session())
    student_repository = PostgresStudentRepository(postgres_manager.get_session())

    issue_repository = PostgresIssueRepository(postgres_manager.get_session())
    issue_comment_repository = PostgresIssueCommentRepository(postgres_manager.get_session())
    issue_comment_query_repository = PostgresIssueCommentQueryRepository(postgres_manager.get_session())
task_manager_repository = MockTaskManagerRepository(database)

# query repositories
# organization_query_repository = MockOrganizationQueryRepository(database)
# owner_query_repository = MockOwnerQueryRepository(database)
# student_query_repository = MockStudentQueryRepository(database)
# issue_query_repository = MockIssueQueryRepository(database)

# postgres query repositories
if postgres_manager is not None:
    organization_query_repository = PostgresOrganizationQueryRepository(postgres_manager.get_session())
    owner_query_repository = PostgresOwnerQueryRepository(postgres_manager.get_session())
    student_query_repository = PostgresStudentQueryRepository(postgres_manager.get_session())
    issue_query_repository = PostgresIssueQueryRepository(postgres_manager.get_session())


# Event handlers
issue_created_event_handler = IssueCreatedHandler(task_manager_factory, task_manager_repository)

# Subscriptions
event_bus.subscribe(
    handler=issue_created_event_handler,
)
