import unittest
from unittest.mock import Mock
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.commands.sign_in_student_command import SignInStudentCommand, \
    SignInStudentCommandRequest, SignInStudentCommandResponse
from madissues_backend.core.students.application.ports.student_repository import StudentRepository
from madissues_backend.core.students.domain.student import Student
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.students.domain.student_mother import StudentMother


class TestSignInStudentCommand(unittest.TestCase):
    def setUp(self):
        # Set up the mock objects for dependencies
        self.student_repository = Mock(spec=StudentRepository)
        self.password_hasher = Mock(spec=PasswordHasher)
        # Create the command object with mocked dependencies
        self.command = SignInStudentCommand(self.student_repository, self.password_hasher)
        # Prepare a valid request object
        self.valid_request = SignInStudentCommandRequest(
            email="john.doe@example.com",
            password="ValidPassword123!"
        )

    def test_successful_signin(self):
        # Mock student with valid credentials
        student = StudentMother.random_student()
        student.password = self.password_hasher.hash("ValidPassword123!")  # Hash the password

        self.student_repository.get_by_email.return_value = student

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Signin should succeed with valid credentials")
        self.assertIsInstance(response.success, SignInStudentCommandResponse, "Response data should be instance of SignInStudentCommandResponse")
        self.assertEqual(response.success.token, student.token, "Token should be correctly assigned in response")
        self.assertEqual(response.success.student_id, str(student.id), "Student ID should be correctly assigned in response")

    def test_invalid_email(self):
        # Mock student repository to return None (no student found)
        self.student_repository.get_by_email.return_value = None

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert failure due to invalid email
        self.assertFalse(response.is_success(), "Signin should fail with invalid email")
        self.assertEqual(response.error.error_code, 1, "Error code should indicate user not found")

    def test_incorrect_password(self):
        # Mock student with valid email but incorrect password
        student = Mock(spec=Student)
        student.check_password = Mock(return_value=False)  # Mocking the check_password method to return False

        self.student_repository.get_by_email.return_value = student

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert failure due to incorrect password
        self.assertFalse(response.is_success(), "Signin should fail with incorrect password")
        self.assertEqual(response.error.error_code, 2, "Error code should indicate incorrect password")


# Uncomment below to run tests
if __name__ == "__main__":
    unittest.main()
