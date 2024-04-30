import unittest

from madissues_backend.core.owners.application.commands.integrate_owner_with_task_manager import \
    IntegrateOwnerWithTaskManagerCommand, IntegrateOwnerWithTaskManagerRequest
from madissues_backend.core.owners.application.commands.sign_up_owner_command import SignUpOwnerCommand, \
    SignUpOwnerCommandRequest
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.application.task_manager_service import TaskManagerServiceFactory
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.mocks.mock_task_manager_service import MockTaskManagerServiceFactory
from madissues_backend.core.shared.infrastructure.openssl.sha256_password_hasher import SHA256PasswordHasher
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator


class TestIntegrateOwnerWithTaskManager(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.owner_repository = MockOwnerRepository(self.db)
        self.event_bus = MockEventBus()
        self.authorization_service = create_mock_authentication_service(self.db)
        self.password_hasher = SHA256PasswordHasher()
        self.token_generator = UUIDTokenGenerator()
        self.command = SignUpOwnerCommand(self.owner_repository, self.password_hasher, self.token_generator)
        self.valid_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="ValidPass123!",
            verify_password="ValidPass123!",
            phone_number="+123456789012"
        )
        self.response = self.command.run(self.valid_request)
        self.authorization = self.authorization_service(self.response.success.token)
        self.task_manager_service_factory = MockTaskManagerServiceFactory()

    def test_integrate_owner_is_successful(self):
        command = IntegrateOwnerWithTaskManagerCommand(self.authorization, self.owner_repository,
                                                       self.task_manager_service_factory)
        response = command.run(IntegrateOwnerWithTaskManagerRequest(
            name="mock",
            api_key="mock-token1"
        ))
        assert response.is_success() is True, "Response must be successful"
        assert response.success.api_key == "mock-token1", "Api token must be saved successfully"
        assert self.owner_repository.get_by_id(
            GenericUUID(self.authorization.get_user_id())).task_manager.token == "mock-token1", "Owner must be saved in db"
    def test_integrate_owner_failed_with_invalid_task_manager(self):
        command = IntegrateOwnerWithTaskManagerCommand(self.authorization, self.owner_repository,
                                                       self.task_manager_service_factory)
        response = command.run(IntegrateOwnerWithTaskManagerRequest(
            name="invalid",
            api_key="mock-token1"
        ))
        print(response)

        assert response.is_error() is True, "Response must be successful"
        self.assertIn("task_manager_name", response.error.error_field, "Api token must be saved successfully")