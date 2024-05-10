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

    def test_organization_is_deleted_without_errors(self):
        # Create organization
        create_command = CreateOrganizationCommand(self.authorization,
                                                   self.organization_repository,
                                                   self.storage_service)

        create_response = create_command.run(CreateOrganizationRequest(
            name="organization1",
            logo="/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxASEhUQEBAV",
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


if __name__ == '__main__':
    unittest.main()
