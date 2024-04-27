import unittest
from unittest.mock import Mock

from pydantic import ValidationError

from madissues_backend.core.owners.application.commands.sign_up_owner_command import SignUpOwnerCommandRequest, \
    SignUpOwnerCommand
from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mock_password_hasher import MockPasswordHasher
from madissues_backend.core.shared.infrastructure.mock_token_generator import MockTokenGenerator


# Assuming these classes are defined and imported as before.

class TestSignUpOwnerCommand(unittest.TestCase):
    def setUp(self):
        # Set up the mock objects for dependencies
        self.owner_repository = Mock(spec=OwnerRepository)
        self.password_hasher = Mock(spec=PasswordHasher)
        self.token_generator = Mock(spec=TokenGenerator)
        # Create the command object with mocked dependencies
        self.command = SignUpOwnerCommand(self.owner_repository, self.password_hasher, self.token_generator)
        # Prepare a valid request object
        self.valid_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="ValidPassword123!",
            verify_password="ValidPassword123!",
            phone_number="1234567890"
        )

    def test_successful_signup(self):
        self.owner_repository.exists_owner_with_email.return_value = False
        self.password_hasher.hash.return_value = "hashed_password"
        self.token_generator.generate.return_value = "auth_token"

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Signup should succeed with valid inputs")
        self.assertIsNotNone(response.success, "Response data should not be None")
        self.assertEqual(response.success.token, "auth_token", "Token should be correctly assigned in response")

    def test_signup_with_existing_email(self):
        # Setup to simulate existing email
        self.owner_repository.exists_owner_with_email.return_value = True

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert failure due to existing email
        self.assertFalse(response.success, "Signup should fail when email already exists")
        self.assertEqual(response.error.error_message, "Email is already in use",
                         "Error message should indicate existing email")

    def test_password_mismatch(self):
        # Prepare a request with mismatched passwords
        mismatched_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.other.doe@example.com",
            password="ValidPassword123!",
            verify_password="InvalidPassword123!",
            phone_number="1234567890"
        )

        self.owner_repository.exists_owner_with_email.return_value = False

        # Execute the command with mismatched passwords
        response = self.command.execute(mismatched_request)

        # Assert failure due to password mismatch
        self.assertFalse(response.success, "Signup should fail when passwords do not match")
        self.assertEqual(response.error.error_message, "Passwords do not match",
                         "Error message should indicate mismatched passwords")

    def test_empty_field_submission(self):
        # Create a request with all fields empty
        empty_request = SignUpOwnerCommandRequest(
            first_name="",
            last_name="",
            email="",
            password="",
            verify_password="",
            phone_number=""
        )

        self.owner_repository.exists_owner_with_email.return_value = False

        # Test validation
        response = self.command.execute(empty_request)
        self.assertTrue(response.is_error())

    def test_special_characters_in_email(self):
        self.token_generator.generate.return_value = "auth_token"
        # Create a request with special characters in the email field
        special_email_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john@@@doe.com",
            password="ValidPassword123!",
            verify_password="ValidPassword123!",
            phone_number="1234567890"
        )

        self.owner_repository.exists_owner_with_email.return_value = False

        response = self.command.execute(special_email_request)
        print(response)
        self.assertFalse(response.success, "Signup should fail with invalid email format")
        self.assertTrue("email" in response.error.error_field, "Signup should fail with invalid email format")

    def test_phone_number_validation(self):
        # Assuming phone number validation is added, testing an invalid phone number
        invalid_phone_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="ValidPassword123!",
            verify_password="ValidPassword123!",
            phone_number="abcde12345"  # Invalid phone number format
        )

        self.owner_repository.exists_owner_with_email.return_value = False
        response = self.command.execute(invalid_phone_request)
        self.assertTrue("phone_number" in response.error.error_field, "Test must fail because phone number")

    def test_password_length_extremes(self):
        # Test with a very short password
        self.owner_repository.exists_owner_with_email.return_value = False

        short_password_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="short",
            verify_password="short",
            phone_number="1234567890"
        )

        # Test with an excessively long password
        long_password_request = SignUpOwnerCommandRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="long" * 50,
            verify_password="long" * 50,
            phone_number="1234567890"
        )

        # Execute tests
        short_response = self.command.execute(short_password_request)
        long_response = self.command.execute(long_password_request)

        # Assert failures
        print(short_response)
        self.assertFalse(short_response.success, "Signup should fail with too short password")
        self.assertFalse(long_response.success, "Signup should fail with too long password")
        self.assertTrue("password" in short_response.error.error_field, "password")
        self.assertTrue("password" in long_response.error.error_field, "password")

    def test_unhandled_exception(self):
        # Simulate an exception in a dependency
        self.owner_repository.exists_owner_with_email.return_value = False
        self.owner_repository.exists_owner_with_email.side_effect = Exception("Unexpected error")

        # Execute the command
        self.assertEqual(self.command.execute(self.valid_request).error.error_code, -1,
                         "Unexpected erros must throw -1 code error")

    def test_end_to_end_command_with_mocks(self):
        db = EntityTable()
        repository = MockOwnerRepository(db)
        hasher = MockPasswordHasher()
        token_generator = MockTokenGenerator()
        command = SignUpOwnerCommand(repository, hasher, token_generator)
        response = command.execute(SignUpOwnerCommandRequest(
            first_name="Pepe",
            last_name="Peña Seco",
            email="josericardopenase@gmail.com",
            password="SecurePassword112233*",
            verify_password="SecurePassword112233*",
            phone_number="599200100"
        ))
        assert response.is_success() == True, "Must succeed"
        self.assertIn(GenericUUID(response.success.owner_id), db.tables["owners"])

# Uncomment below to run tests
# if __name__ == "__main__":
#     unittest.main()
