import unittest
from unittest.mock import MagicMock

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.task_manager.application.commands.integrate_organization_with_task_manager import IntegrateOrganizationWithTaskManagerCommand, IntegrateOrganizationWithTaskManagerRequest
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_repository import \
    MockTaskManagerRepository
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_service import \
    InMemoryTaskManagerService, InMemoryTaskManagerFactory


class TestIntegrateOrganizationWithTaskManagerCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_task_managers_table")
        self.repository = MockTaskManagerRepository(self.db)
        self.authentication = create_mock_authentication_service(self.db)
        self.auth = self.authentication("1d372590-a034-4e05-b1e8-02a9e91068f3")
        self.factory = InMemoryTaskManagerFactory()

    def test_integration_successful(self):
        print(self.db.tables)
        command = IntegrateOrganizationWithTaskManagerCommand(self.auth, self.repository, self.factory)
        response = command.run(IntegrateOrganizationWithTaskManagerRequest(
            organization_id="cc164174-07f7-4cd4-8a7e-43c96d9b825a",
            task_manager="trello",
            api_key="invalid_api_key"
        ))
        print(response)

    # Add more tests here...

if __name__ == '__main__':
    unittest.main()