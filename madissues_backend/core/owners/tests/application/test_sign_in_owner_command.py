import unittest
from unittest.mock import Mock

from madissues_backend.core.owners.application.commands.sign_in_owner_command import SignInOwnerCommandRequest, \
    SignInOwnerCommand
from madissues_backend.core.owners.application.commands.sign_up_owner_command import SignUpOwnerCommandRequest, \
    SignUpOwnerCommand
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.shared.infrastructure.openssl.sha256_password_hasher import SHA256PasswordHasher
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator


class TestSignUpOwnerCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.owner_repository = MockOwnerRepository(self.db)
        self.password_hasher = SHA256PasswordHasher()
        self.token_generator = UUIDTokenGenerator()
        self.command = SignUpOwnerCommand(self.owner_repository, self.password_hasher, self.token_generator)

        # Valid request setup
        self.valid_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="ValidPass123!",
            verify_password="ValidPass123!",
            phone_number="+123456789012"
        )
        self.response = self.command.run(self.valid_request)

    def test_login_succesfull_with_valid_credentials(self):
        request = SignInOwnerCommandRequest(
            email="john.doe@example.com",
            password="ValidPass123!"
        )
        command = SignInOwnerCommand(self.owner_repository, self.password_hasher)
        response = command.run(request)
        assert response.is_success() is True, "The result must be valid with valid credentials"
        assert response.success.token is self.response.success.token, "Tokens must be the same"

    def test_login_failed_with_invalid_mail(self):
        request = SignInOwnerCommandRequest(
            email="john.doe@example.comm",
            password="ValidPass123!"
        )
        command = SignInOwnerCommand(self.owner_repository, self.password_hasher)
        response = command.run(request)
        assert response.is_success() is False, "The result must be valid with valid credentials"
        assert response.error.error_code is 1, "Error code must be caused by mail"

    def test_login_failed_with_invalid_password(self):
        request = SignInOwnerCommandRequest(
            email="john.doe@example.com",
            password="ValidPass123"
        )
        command = SignInOwnerCommand(self.owner_repository, self.password_hasher)
        response = command.run(request)
        assert response.is_success() is False, "The result must be valid with valid credentials"
        assert response.error.error_code is 2, "Error code must be caused by password"
