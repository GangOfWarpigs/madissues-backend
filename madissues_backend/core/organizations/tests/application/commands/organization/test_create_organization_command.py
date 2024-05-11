import unittest

from madissues_backend.core.organizations.application.commands.organization.create_organization_command import \
    CreateOrganizationCommand, CreateOrganizationRequest
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


class TestCreateOrganizationCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_owner_created")
        self.event_bus = MockEventBus()
        self.authorization_service = create_mock_authentication_service(self.db)
        self.password_hasher = SHA256PasswordHasher()
        self.token_generator = UUIDTokenGenerator()
        self.authorization = self.authorization_service("1d372590-a034-4e05-b1e8-02a9e91068f3")
        self.organization_repository = MockOrganizationRepository(self.db)
        self.storage_service = LocalStorageService("../../../../../../media")

    def tearDown(self):
        self.event_bus.events = []


    def test_organization_is_created_without_errors(self):
        command = CreateOrganizationCommand(self.authorization,
                                            self.organization_repository, self.storage_service)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo="iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))

        assert response.is_success() == True, "Command must succed"
        assert response.success.logo != "default_organization_logo.png"
        assert self.organization_repository.get_by_id(GenericUUID(response.success.id)) is not None, "Must be not None"

    def test_organization_is_created_with_non_valid_chars(self):
        command = CreateOrganizationCommand(self.authorization,
                                            self.organization_repository, self.storage_service)
        response = command.run(CreateOrganizationRequest(
            name="string",
            description="string",
            contact_info="string",
            primary_color="string",
            secondary_color="string"
        ))

        print(response)
        assert response.is_error() == True, "Command must succed"

    def test_create_organization_without_being_owner(self):
        command = CreateOrganizationCommand(self.authorization_service("mock-token"),
                                            self.organization_repository, self.storage_service)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo="b64",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))

        assert response.is_error() == True, "Command must fail"
        assert response.error.error_code == 403, "Command must fail because you are not authorized"

    def test_create_organization_without_logo(self):
        command = CreateOrganizationCommand(self.authorization,
                                            self.organization_repository, self.storage_service)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))

        assert response.is_success() == True, "Command must succed"
        assert response.success.logo == "default_organization_logo.png", "Logo must be the default one"

    def test_create_organization_failed_with_empty_name(self):
        command = CreateOrganizationCommand(self.authorization, self.organization_repository, self.storage_service)
        response = command.run(CreateOrganizationRequest(
            name="",
            logo="data:image/gif;base64,R0lGODlhAQABAAAAACw=",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))
        assert response.is_error() is True, "Organization should not be created when name is empty"
        assert response.error.error_code == 1, "Error code must be caused by empty name"
        self.assertIn("name", response.error.error_field, "Must be caused by name")

    def test_create_organization_failed_with_empty_description(self):
        command = CreateOrganizationCommand(self.authorization, self.organization_repository, self.storage_service)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo="b64",
            description="",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))
        assert response.is_error() is True, "Organization should not be created when description is empty"
        assert response.error.error_code == 1, "Error code must be caused by empty description"
        self.assertIn("description", response.error.error_field, "Must be caused by description")

    def test_create_organization_failed_with_empty_logo(self):
        command = CreateOrganizationCommand(self.authorization, self.organization_repository, self.storage_service)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            description="pepe",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))
        assert response.is_error() is False, "Organization should not be created when logo is invalid"
