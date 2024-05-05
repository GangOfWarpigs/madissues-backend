import unittest
from unittest.mock import MagicMock

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.task_manager.application.commands.integrate_organization_with_task_manager import IntegrateOrganizationWithTaskManagerCommand, IntegrateOrganizationWithTaskManagerRequest
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_repository import \
    MockTaskManagerRepository
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_service import \
    InMemoryTaskManagerService, MockTaskManagerFactory


class TestIntegrateOrganizationWithTaskManagerCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_task_managers_table")
        self.repository = MockTaskManagerRepository(self.db)
        self.authentication = create_mock_authentication_service(self.db)
        self.auth = self.authentication("1d372590-a034-4e05-b1e8-02a9e91068f3")
        self.factory = MockTaskManagerFactory()

    def test_integration_successful(self):
        print(self.db.tables)
        command = IntegrateOrganizationWithTaskManagerCommand(self.auth, self.repository, self.factory)
        response = command.run(IntegrateOrganizationWithTaskManagerRequest(
            organization_id="cc164174-07f7-4cd4-8a7e-43c96d9b825a",
            task_manager="trello",
            api_key="valid_api_key"
        ))

        assert response.is_success() == True, "Must be successful"
        assert response.success.message is not None, "Message must have something"
        assert self.repository.is_there_a_task_manager_for_organization("cc164174-07f7-4cd4-8a7e-43c96d9b825a") == True

    def test_integration_not_successful(self):
        command = IntegrateOrganizationWithTaskManagerCommand(self.auth, self.repository, self.factory)
        response = command.run(IntegrateOrganizationWithTaskManagerRequest(
            organization_id="cc164174-07f7-4cd4-8a7e-43c96d9b825a",
            task_manager="trello",
            api_key="looool"
        ))

        print(response)

        assert response.is_error() is True, "Must be error"
        assert response.error.error_code == 4, "Message must have something"

    def test_integration_not_owner(self):
        command = IntegrateOrganizationWithTaskManagerCommand(self.authentication("invalid_token"), self.repository, self.factory)
        response = command.run(IntegrateOrganizationWithTaskManagerRequest(
            organization_id="cc164174-07f7-4cd4-8a7e-43c96d9b825a",
            task_manager="trello",
            api_key="looool"
        ))
        assert response.is_error() is True, "Must be error"
        assert response.error.error_code == 403, "Message must have something"

    def test_there_is_already_an_integration(self):
        command = IntegrateOrganizationWithTaskManagerCommand(self.auth, self.repository, self.factory)
        response = command.run(IntegrateOrganizationWithTaskManagerRequest(
            organization_id="cc164174-07f7-4cd4-8a7e-43c96d9b825a",
            task_manager="trello",
            api_key="valid_api_key"
        ))
        print(self.db.tables)
        command = IntegrateOrganizationWithTaskManagerCommand(self.auth, self.repository, self.factory)
        response = command.run(IntegrateOrganizationWithTaskManagerRequest(
            organization_id="cc164174-07f7-4cd4-8a7e-43c96d9b825a",
            task_manager="trello",
            api_key="valid_api_key"
        ))
        assert response.is_error() is True, "Must be error"
        assert response.error.error_code == 3, "Message must have something"
        assert self.repository.is_there_a_task_manager_for_organization("cc164174-07f7-4cd4-8a7e-43c96d9b825a") == True

if __name__ == '__main__':
    unittest.main()