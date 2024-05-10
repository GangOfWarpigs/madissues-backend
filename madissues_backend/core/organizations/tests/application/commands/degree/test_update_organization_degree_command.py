import unittest

from madissues_backend.core.organizations.application.commands.degree.create_organization_degree_command import \
    CreateOrganizationDegreeRequest, CreateOrganizationDegreeResponse, CreateOrganizationDegreeCommand
from madissues_backend.core.organizations.application.commands.degree.update_organization_degree_command import \
    UpdateOrganizationDegreeRequest, UpdateOrganizationDegreeResponse, UpdateOrganizationDegreeCommand
from madissues_backend.core.organizations.domain.organization_mother import OrganizationMother
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus


class TestUpdateOrganizationDegreeCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.organization_repository = MockOrganizationRepository(self.db)
        self.event_bus = MockEventBus()
        self.organization = self.organization_repository.get_by_id(
            GenericUUID("cc164174-07f7-4cd4-8a7e-43c96d9b825a"))
        self.owner = self.db.tables['owners'][GenericUUID("83d150fe-84f4-4a22-a109-5704342c589c")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.owner.token)

    def test_execute_success(self):
        # Arrange
        degree_request = CreateOrganizationDegreeRequest(
            organization_id=str(self.organization.id),
            name="Physics"
        )
        create_degree_command = CreateOrganizationDegreeCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )
        response_create = create_degree_command.execute(degree_request)
        self.assertTrue(response_create.is_success(), "Degree should be created successfully")
        degree_id = response_create.success.id

        # Update degree
        updated_name = "Mathematics"
        update_request = UpdateOrganizationDegreeRequest(
            degree_id=degree_id,
            organization_id=str(self.organization.id),
            name=updated_name
        )
        update_command = UpdateOrganizationDegreeCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response_update = update_command.execute(update_request)

        # Assert
        self.assertTrue(response_update.is_success(), "Degree should be updated successfully")
        self.assertEqual(response_update.success.degree_id, degree_id, "Degree ID should match")
        self.assertEqual(response_update.success.organization_id, str(self.organization.id),
                         "Organization ID should match")
        self.assertEqual(response_update.success.name, updated_name, "Degree name should match")
        # Check if the event is triggered
        self.assertEqual(len(self.event_bus.events), 2, "Should trigger an event")

        # Check if the degree is updated in the organization
        organization = self.organization_repository.get_by_id(GenericUUID(update_request.organization_id))
        updated_degree = organization.get_degree_by_id(GenericUUID(degree_id))
        self.assertIsNotNone(updated_degree, "Updated degree should exist in the organization")
        self.assertEqual(updated_degree.name, updated_name, "Degree name should match")

    def test_execute_invalid_organization_id(self):
        # Reset event bus
        self.event_bus.events = []
        # Arrange
        degree_request = CreateOrganizationDegreeRequest(
            organization_id=str(self.organization.id),
            name="Physics"
        )
        create_degree_command = CreateOrganizationDegreeCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )
        response_create = create_degree_command.execute(degree_request)
        self.assertTrue(response_create.is_success(), "Degree should be created successfully")
        degree_id = response_create.success.id

        # Update degree with invalid organization ID
        updated_name = "Mathematics"
        update_request = UpdateOrganizationDegreeRequest(
            degree_id=degree_id,
            organization_id="invalid_id",
            name=updated_name
        )
        update_command = UpdateOrganizationDegreeCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response_update = update_command.execute(update_request)

        # Assert
        self.assertTrue(not response_update.is_success(), "Organization ID should be invalid")
        self.assertEqual(response_update.error.error_message, "Invalid organization ID",
                         "Should return 'Invalid organization ID'")
        self.assertEqual(len(self.event_bus.events), 1, "Should not trigger an event")

    def test_execute_unauthorized(self):
        # Reset event bus
        self.event_bus.events = []
        # Arrange
        degree_request = CreateOrganizationDegreeRequest(
            organization_id=str(self.organization.id),
            name="Physics"
        )
        create_degree_command = CreateOrganizationDegreeCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )
        response_create = create_degree_command.execute(degree_request)
        self.assertTrue(response_create.is_success(), "Degree should be created successfully")
        degree_id = response_create.success.id

        # Update degree with unauthorized user
        unauthorized_owner = self.db.tables['owners'][GenericUUID("ca7b384c-0ae9-489f-90c6-a18a6781dcd0")]
        authentication_service = create_mock_authentication_service(self.db)(unauthorized_owner.token)
        updated_name = "Mathematics"
        update_request = UpdateOrganizationDegreeRequest(
            degree_id=degree_id,
            organization_id=str(self.organization.id),
            name=updated_name
        )
        update_command = UpdateOrganizationDegreeCommand(
            authentication_service=authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act (raises an exception)
        response_update = update_command.execute(update_request)

        # Assert
        self.assertTrue(not response_update.is_success(), "User should not be authorized")
        self.assertEqual(response_update.error.error_message, "You are not the owner of the organization",
                         "Should return 'User must be an owner of the organization'")
        self.assertEqual(len(self.event_bus.events), 1, "Should not trigger an event")


if __name__ == '__main__':
    unittest.main()
