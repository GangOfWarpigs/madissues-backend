import unittest

from madissues_backend.core.organizations.application.commands.degree.delete_organization_degree_command import \
    DeleteOrganizationDegreeRequest, DeleteOrganizationDegreeResponse, DeleteOrganizationDegreeCommand
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus


class TestDeleteOrganizationDegreeCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.organization_repository = MockOrganizationRepository(self.db)
        self.event_bus = MockEventBus()
        self.organization = self.organization_repository.get_by_id(GenericUUID("cc164174-07f7-4cd4-8a7e-43c96d9b825a"))
        self.owner = self.db.tables['owners'][GenericUUID("83d150fe-84f4-4a22-a109-5704342c589c")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.owner.token)

    def test_execute_success(self):
        # Arrange
        degree_id = str(self.organization.degrees[0].id)
        degree_request = DeleteOrganizationDegreeRequest(
            organization_id=str(self.organization.id),
            degree_id=degree_id
        )
        command = DeleteOrganizationDegreeCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(degree_request)

        # Assert
        self.assertTrue(response.is_success(), "Degree should be deleted successfully")
        self.assertEqual(response.success.degree_id, degree_id, "Degree ID should match")
        self.assertEqual(response.success.organization_id, str(self.organization.id), "Organization ID should match")

        # Degree should be removed from the organization
        organization = self.organization_repository.get_by_id(GenericUUID(degree_request.organization_id))
        self.assertTrue(all(degree.id != GenericUUID(degree_id) for degree in organization.degrees),
                        "Degree should be removed from the organization")
        self.assertEqual(len(self.event_bus.events), 1, "Should trigger an event")

    def test_execute_invalid_organization_id(self):
        # Arrange
        degree_id = str(self.organization.degrees[0].id)
        degree_request = DeleteOrganizationDegreeRequest(
            organization_id="invalid_id",
            degree_id=degree_id
        )
        command = DeleteOrganizationDegreeCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(degree_request)

        # Assert
        self.assertTrue(not response.success, "Organization ID should be invalid")
        self.assertEqual(response.error.error_message, "Invalid organization ID",
                         "Should return 'Invalid organization ID'")

    def test_execute_unauthorized(self):
        # Arrange
        degree_id = str(self.organization.degrees[0].id)
        unauthorized_owner = self.db.tables['owners'][GenericUUID("ca7b384c-0ae9-489f-90c6-a18a6781dcd0")]
        authentication_service = create_mock_authentication_service(self.db)(unauthorized_owner.token)
        degree_request = DeleteOrganizationDegreeRequest(
            organization_id=str(self.organization.id),
            degree_id=degree_id
        )
        command = DeleteOrganizationDegreeCommand(
            authentication_service=authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act (raises an exception)
        response = command.execute(degree_request)

        # Assert
        self.assertTrue(not response.success, "User should not be authorized")
        self.assertEqual(response.error.error_message, "You are not the owner of the organization",
                         "Should return 'User must be an owner of the organization'")


if __name__ == '__main__':
    unittest.main()
