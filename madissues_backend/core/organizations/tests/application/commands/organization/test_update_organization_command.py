import unittest

from madissues_backend.core.organizations.application.commands.organization.create_organization_command import \
    CreateOrganizationCommand, CreateOrganizationRequest
from madissues_backend.core.organizations.application.commands.organization.update_organization_info_command import \
    UpdateOrganizationCommand, UpdateOrganizationRequest
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.mocks.mock_storage_service import MockStorageService
from madissues_backend.core.shared.infrastructure.openssl.sha256_password_hasher import SHA256PasswordHasher
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator


class TestUpdateOrganizationCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_owner_created")
        self.event_bus = MockEventBus()
        self.authorization_service = create_mock_authentication_service(self.db)
        self.password_hasher = SHA256PasswordHasher()
        self.token_generator = UUIDTokenGenerator()
        self.authorization = self.authorization_service("1d372590-a034-4e05-b1e8-02a9e91068f3")
        self.organization_repository = MockOrganizationRepository(self.db)
        self.storage_service = MockStorageService()

        # Create an organization
        command = CreateOrganizationCommand(self.authorization,
                                            self.organization_repository, self.storage_service)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo=",iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))
        self.organization_id = response.success.id

    def tearDown(self):
        self.event_bus.events = []

    def test_organization_is_updated_without_errors(self):
        # Reset the event bus
        self.event_bus.events = []
        command = UpdateOrganizationCommand(self.authorization,
                                            self.organization_repository,
                                            self.storage_service,
                                            self.event_bus)
        response = command.run(UpdateOrganizationRequest(
            organization_id=self.organization_id,
            name="updated_organization_name",
            description="updated organization description",
            contact_info="updated contact info",
            primary_color="#000000",
            secondary_color="#ffffff"
        ))

        self.assertTrue(response.is_success(), "Command must succeed")
        updated_organization = self.organization_repository.get_by_id(GenericUUID(self.organization_id))
        self.assertEqual(updated_organization.name, "updated_organization_name")
        self.assertEqual(updated_organization.description, "updated organization description")
        self.assertEqual(updated_organization.contact_info, "updated contact info")
        self.assertEqual(updated_organization.primary_color, "#000000")
        self.assertEqual(updated_organization.secondary_color, "#ffffff")
        # Assert an event was published
        self.assertEqual(len(self.event_bus.events), 1)


    def test_organization_is_updated_with_non_valid_chars(self):
        # Reset the event bus
        self.event_bus.events = []
        command = UpdateOrganizationCommand(self.authorization,
                                            self.organization_repository,
                                            self.storage_service,
                                            self.event_bus)
        response = command.run(UpdateOrganizationRequest(
            organization_id=str(GenericUUID.next_id()),
            name="",
            description="",
            contact_info="",
            primary_color="",
            secondary_color=""
        ))

        self.assertTrue(response.is_error(), "Command must fail")
        # Assert no event was published
        self.assertEqual(len(self.event_bus.events), 0)

    def test_update_organization_without_being_owner(self):
        # Reset the event bus
        self.event_bus.events = []
        command = UpdateOrganizationCommand(self.authorization_service("mock-token"),
                                            self.organization_repository,
                                            self.storage_service,
                                            self.event_bus)
        response = command.run(UpdateOrganizationRequest(
            organization_id=str(GenericUUID.next_id()),
            name="updated_organization_name",
            description="updated organization description",
            contact_info="updated contact info",
            primary_color="#000000",
            secondary_color="#ffffff"
        ))

        self.assertTrue(response.is_error(), "Command must fail")
        self.assertEqual(response.error.error_code, 403, "Command must fail because you are not authorized")
        # Assert no event was published
        self.assertEqual(len(self.event_bus.events), 0)


    def test_update_organization_with_non_existing_id(self):
        # Reset the event bus
        self.event_bus.events = []
        command = UpdateOrganizationCommand(self.authorization,
                                            self.organization_repository,
                                            self.storage_service,
                                            self.event_bus)
        response = command.run(UpdateOrganizationRequest(
            organization_id=str(GenericUUID.next_id()),
            name="updated_organization_name",
            description="updated organization description",
            contact_info="updated contact info",
            primary_color="#000000",
            secondary_color="#ffffff"
        ))

        self.assertTrue(response.is_error(), "Command must fail")
        self.assertEqual(response.error.error_code, 404, "Command must fail because organization not found")
        # Assert no event was published
        self.assertEqual(len(self.event_bus.events), 0)


if __name__ == '__main__':
    unittest.main()
