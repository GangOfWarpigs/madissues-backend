import unittest
from unittest.mock import MagicMock
from madissues_backend.core.organizations.application.commands.organization.create_organization_command import \
    CreateOrganizationCommand, CreateOrganizationRequest
from madissues_backend.core.organizations.application.commands.organization.delete_organization_command import \
    DeleteOrganizationCommand, DeleteOrganizationRequest
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService


class TestDeleteOrganizationCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_owner_created")
        self.event_bus = MagicMock()
        self.authorization_service = create_mock_authentication_service(self.db)
        self.authorization = self.authorization_service("1d372590-a034-4e05-b1e8-02a9e91068f3")
        self.organization_repository = MockOrganizationRepository(self.db)
        self.storage_service = LocalStorageService("../../../../../../media")

    def tearDown(self):
        self.event_bus.events = []

    def test_organization_is_deleted_without_errors(self):
        # Create organization
        create_command = CreateOrganizationCommand(self.authorization,
                                                   self.organization_repository,
                                                   self.storage_service)

        create_response = create_command.run(CreateOrganizationRequest(
            name="organization1",
            logo=",iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))

        assert create_response.is_success() is True, "Organization must be created successfully"

        # Delete organization
        delete_command = DeleteOrganizationCommand(self.authorization,
                                                   self.organization_repository,
                                                   self.storage_service)

        delete_response = delete_command.run(
            DeleteOrganizationRequest(
                organization_id=create_response.success.id)
        )

        assert delete_response.is_success() is True, "Organization must be deleted successfully"
        assert self.organization_repository.get_by_id(GenericUUID(create_response.success.id)) is None, \
            "Organization must not exist in the repository"

    def test_delete_nonexistent_organization(self):
        # Delete organization with a non-existent ID
        delete_command = DeleteOrganizationCommand(self.authorization,
                                                   self.organization_repository,
                                                   self.storage_service)

        invalid_organization_UUID = GenericUUID.next_id()
        # Check that the organization does not exist
        assert self.organization_repository.get_by_id(invalid_organization_UUID) is None, \
            "Organization must not exist in the repository"

        delete_response = delete_command.run(
            DeleteOrganizationRequest(
                organization_id=str(invalid_organization_UUID))
        )

        assert delete_response.is_error() is True, "Organization deletion should fail"
        assert delete_response.error.error_code == 404, "Error code must indicate 'not found'"
        assert delete_response.error.error_message == "Organization not found", "Error message must indicate 'not found'"

    def test_delete_organization_without_being_owner(self):
        # Create organization
        create_command = CreateOrganizationCommand(self.authorization,
                                                   self.organization_repository,
                                                   self.storage_service)

        create_response = create_command.run(CreateOrganizationRequest(
            name="organization1",
            logo=",iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))

        assert create_response.is_success() is True, "Organization must be created successfully"

        mock_token = GenericUUID.next_id()
        # Check that the token is not the owner
        assert self.authorization_service(mock_token) != create_response.success.owner_id, \
            "Token must not be the owner of the organization"

        # Delete organization without being the owner
        delete_command = DeleteOrganizationCommand(self.authorization_service("mock-token"),
                                                   self.organization_repository,
                                                   self.storage_service)

        delete_response = delete_command.run(
            DeleteOrganizationRequest(
                organization_id=create_response.success.id)
        )

        assert delete_response.is_error() is True, "Organization deletion should fail"
        assert delete_response.error.error_code == 403, "Error code must indicate 'forbidden'"
        assert delete_response.error.error_message == "User must be a owner", \
            "Error message must indicate 'forbidden'"


if __name__ == '__main__':
    unittest.main()
