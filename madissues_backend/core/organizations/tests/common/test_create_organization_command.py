import unittest
from unittest.mock import Mock

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
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator

# FIXME: delete this imports using EntityTableMother
from madissues_backend.core.owners.application.commands.sign_up_owner_command import SignUpOwnerCommandRequest, \
    SignUpOwnerCommand
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository


class TestCreateOrganizationCommand(unittest.TestCase):
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
        self.organization_repository = MockOrganizationRepository(self.db)
        self.storage = MockStorageService()

    def test_organization_is_created_without_errors(self):
        command = CreateOrganizationCommand(self.authorization,
                                            self.organization_repository, self.storage)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo="b64",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))

        assert response.is_success() == True, "Command must succed"
        assert response.success.logo == "uploaded_was_called.png"
        assert self.organization_repository.get_by_id(GenericUUID(response.success.id)) is not None, "Must be not None"

    def test_organization_is_created_with_non_valid_chars(self):
        command = CreateOrganizationCommand(self.authorization,
                                            self.organization_repository, self.storage)
        response = command.run(CreateOrganizationRequest(
            name="string",
            description="string",
            contact_info="string",
            primary_color="string",
            secondary_color="string"
        ))

        print(response)
        assert response.is_error() == True, "Command must succed"

    def test_organization_without_beeing_owner(self):
        command = CreateOrganizationCommand(self.authorization_service("mock-token"),
                                            self.organization_repository, self.storage)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo="b64",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))

        assert response.is_error() == True, "Command must fail"
        assert response.error.error_code ==403, "Command must fail because you are not authorized"


    def test_organization_without_logo(self):
        command = CreateOrganizationCommand(self.authorization,
                                            self.organization_repository, self.storage)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            description="this is my organization",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))

        assert response.is_success() == True, "Command must succed"
        assert response.success.logo == None, "Logo must be none"

    def test_create_organization_failed_with_empty_name(self):
        command = CreateOrganizationCommand(self.authorization, self.organization_repository, self.storage)
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
        command = CreateOrganizationCommand(self.authorization, self.organization_repository, self.storage)
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

    def test_create_organization_failed_with_empty_description(self):
        command = CreateOrganizationCommand(self.authorization, self.organization_repository, self.storage)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo="data:image/gif;base64,R0lGODlhAQABAAAAACw=",
            description="",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))
        assert response.is_error() is True, "Organization should not be created when description is empty"
        assert response.error.error_code == 1, "Error code must be caused by empty description"
        self.assertIn("description", response.error.error_field, "Must be caused by description")

    def test_create_organization_failed_with_empty_description(self):
        command = CreateOrganizationCommand(self.authorization, self.organization_repository, self.storage)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo="data:image/gif;base64,R0lGODlhAQABAAAAACw=",
            description="",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))
        assert response.is_error() is True, "Organization should not be created when description is empty"
        assert response.error.error_code == 1, "Error code must be caused by empty description"
        self.assertIn("description", response.error.error_field, "Must be caused by description")

    def test_create_organization_failed_with_empty_logo(self):
        command = CreateOrganizationCommand(self.authorization, self.organization_repository, self.storage)
        response = command.run(CreateOrganizationRequest(
            name="organization1",
            logo="",
            description="pepe",
            contact_info="contact info",
            primary_color="#f5f5f5",
            secondary_color="#f5f5f5"
        ))
        assert response.is_error() is True, "Organization should not be created when logo is invalid"
