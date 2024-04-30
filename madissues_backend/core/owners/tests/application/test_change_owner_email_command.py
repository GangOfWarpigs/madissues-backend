import unittest
from unittest.mock import Mock

from madissues_backend.core.owners.application.commands.change_owner_email import ChangeOwnerEmailCommand, \
    ChangeOwnerEmailRequest
from madissues_backend.core.owners.application.commands.sign_up_owner_command import SignUpOwnerCommandRequest, \
    SignUpOwnerCommand
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.openssl.sha256_password_hasher import SHA256PasswordHasher
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator


class TestChangeOwnerEmailCommand(unittest.TestCase):
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

    def test_change_email_successful_with_valid_credentials(self):
        change_email = "pepe@pepe.com"
        request = ChangeOwnerEmailRequest(
            email="pepe@pepe.com"
        )
        command = ChangeOwnerEmailCommand(self.authorization, self.owner_repository, self.event_bus)
        response = command.run(request)
        print(response)
        assert response.success.email is change_email, "Email should be updated"
        assert self.db.tables.get("owners").get(
            GenericUUID(response.success.id)).email is change_email, "Email should be changed in db"
        assert len(self.event_bus.events) == 1, "Should be triggered an event"

    def test_change_invalid_email_does_not_work(self):
        change_email = "pepe"
        request = ChangeOwnerEmailRequest(
            email=change_email
        )
        command = ChangeOwnerEmailCommand(self.authorization, self.owner_repository, self.event_bus)
        response = command.run(request)
        assert response.is_error() is True, "Email should not update when not valid email"
        self.assertIn("email", response.error.error_field, "Email cannot be invalid")

    def test_failed_authorization_wont_work(self):
        change_email = "pepe"
        request = ChangeOwnerEmailRequest(
            email=change_email
        )
        command = ChangeOwnerEmailCommand(self.authorization_service("mitokeninventado"), self.owner_repository, self.event_bus)
        response = command.run(request)
        assert response.is_error() is True, "Email should not update when not valid email"
        assert response.error.error_code == 403, "Should not be authorized if not valid token"
