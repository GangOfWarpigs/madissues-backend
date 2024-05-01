import unittest
from unittest.mock import Mock

from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.commands.sign_up_student_command import SignUpStudentCommand, \
    SignUpStudentCommandRequest, SignUpStudentCommandResponse
from madissues_backend.core.students.application.ports.student_repository import StudentRepository


class TestSignUpStudentCommand(unittest.TestCase):
    def setUp(self):
        # Set up the mock objects for dependencies
        self.student_repository = Mock(spec=StudentRepository)
        self.password_hasher = Mock(spec=PasswordHasher)
        self.token_generator = Mock(spec=TokenGenerator)
        # Create the command object with mocked dependencies
        self.command = SignUpStudentCommand(self.student_repository, self.password_hasher, self.token_generator)
        # Prepare a valid request object
        self.valid_request = SignUpStudentCommandRequest(
            organization_id=str(GenericUUID.next_id()),
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="ValidPassword123!",
            verify_password="ValidPassword123!",
            phone_number="1234567890",
            degreeId=str(GenericUUID.next_id()),
            started_studies_date="2024-05-01"
        )

    def test_successful_signup(self):
        self.student_repository.exists_with_email.return_value = False
        self.student_repository.can_student_join_organization.return_value = True
        self.password_hasher.hash.return_value = "hashed_password"
        self.token_generator.generate.return_value = "auth_token"

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Signup should succeed with valid inputs")
        self.assertIsInstance(response.success, SignUpStudentCommandResponse,
                              "Response data should be instance of SignUpStudentCommandResponse")
        self.assertEqual(response.success.token, "auth_token", "Token should be correctly assigned in response")

    def test_signup_with_existing_email(self):
        # Setup to simulate existing email
        self.student_repository.exists_with_email.return_value = True

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert failure due to existing email
        self.assertFalse(response.is_success(), "Signup should fail when email already exists")
        self.assertEqual(2, response.error.error_code, "Error code should indicate existing email")

    def test_password_mismatch(self):
        # Prepare a request with mismatched passwords

        mismatched_request = SignUpStudentCommandRequest(
            organization_id="organization_id",
            email="john.other.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="ValidPassword123!",
            verify_password="InvalidPassword123!",
            phone_number="1234567890",
            degreeId="degree_id",
            started_studies_date="2024-05-01"
        )

        self.student_repository.exists_with_email.return_value = False
        self.student_repository.can_student_join_organization.return_value = True

        # Execute the command with mismatched passwords
        response = self.command.execute(mismatched_request)

        # Assert failure due to password mismatch
        self.assertFalse(response.is_success(), "Signup should fail when passwords do not match")
        self.assertEqual(3, response.error.error_code, "Error code should indicate mismatched passwords")

    def test_organization_membership_check(self):
        # Setup to simulate organization membership check failure
        self.student_repository.exists_with_email.return_value = False
        self.student_repository.can_student_join_organization.return_value = False

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert failure due to organization membership check
        self.assertFalse(response.is_success(), "Signup should fail when student cannot join organization")
        self.assertEqual(4, response.error.error_code, "Error code should indicate inability to join organization")

    def test_empty_field_submission(self):
        # Create a request with all fields empty

        empty_request = SignUpStudentCommandRequest(
            organization_id="",
            email="",
            first_name="",
            last_name="",
            password="",
            verify_password="",
            phone_number="",
            degreeId="",
            started_studies_date=""
        )

        # Test validation
        response = self.command.execute(empty_request)
        self.assertFalse(response.is_success(), "Signup should fail with empty fields")


if __name__ == '__main__':
    unittest.main()
