import unittest
from unittest.mock import Mock

from madissues_backend.core.owners.application.commands.sign_up_owner_command import SignUpOwnerCommandRequest, \
    SignUpOwnerCommand
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.shared.domain.token_generator import TokenGenerator


class TestSignUpOwnerCommand(unittest.TestCase):
    def setUp(self):
        self.owner_repository = Mock()
        self.password_hasher = Mock(PasswordHasher)
        self.token_generator = Mock(TokenGenerator)
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

    def test_successful_signup(self):
        self.owner_repository.get_owner_by_email.return_value = False
        response = self.command.execute(self.valid_request)
        self.assertTrue("token" in response.data)

    def test_signup_with_existing_email(self):
        self.owner_repository.exists_owner_with_email.return_value = True
        response = self.command.execute(self.valid_request)
        self.assertEqual(response.message, "Email is already in use")

    def test_password_mismatch(self):
        mismatched_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.other@example.com",
            password="ValidPass123!",
            verify_password="InvalidPass123!",
            phone_number="+123456789012"
        )
        self.owner_repository.exists_owner_with_email.return_value = False
        response = self.command.execute(mismatched_request)
        self.assertEqual(response.message, "Passwords do not match")

    def test_invalid_email_format(self):
        invalid_email_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="invalid_email",
            password="ValidPass123!",
            verify_password="ValidPass123!",
            phone_number="+123456789012"
        )
        with self.assertRaises(ValueError):
            self.command.execute(invalid_email_request)

    def test_invalid_password_length(self):
        invalid_password_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="short",
            verify_password="short",
            phone_number="+123456789012"
        )
        with self.assertRaises(ValueError):
            self.command.execute(invalid_password_request)

    def test_invalid_phone_format(self):
        invalid_phone_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="ValidPass123!",
            verify_password="ValidPass123!",
            phone_number="12345"  # Invalid format
        )
        with self.assertRaises(ValueError):
            self.command.execute(invalid_phone_request)