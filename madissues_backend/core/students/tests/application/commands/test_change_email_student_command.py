import unittest

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.students.application.commands.change_student_email_command import ChangeStudentEmailCommand, \
    ChangeStudentEmailRequest
from madissues_backend.core.students.domain.student_mother import StudentMother
from madissues_backend.core.students.infrastructure.mocks.mock_student_repository import MockStudentRepository


class TestChangeStudentEmailCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.student_repository = MockStudentRepository(self.db)
        self.event_bus = MockEventBus()
        self.student = StudentMother.random_student()

        # Initialize authentication service with a valid student token (get class and instantiate)
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)

        self.command = ChangeStudentEmailCommand(self.authentication_service, self.student_repository, self.event_bus)
        self.valid_request = ChangeStudentEmailRequest(
            email="new_email@mail.com"
        )

    def test_change_student_email_successful(self):
        # Add student to repository
        self.student_repository.add(self.student)

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Email should be updated")
        self.assertEqual(response.success.email, self.valid_request.email,
                         "Email should be correctly assigned in response")
        self.assertEqual(self.db.tables.get("students").get(self.student.id).email, self.valid_request.email,
                         "Email should be changed in db")
        self.assertEqual(len(self.event_bus.events), 1, "Should be triggered an event")

    def test_change_student_email_unauthenticated(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Execute the command with the valid request
        response = self.command.execute(self.valid_request)

        # Assert error and check response data
        self.assertTrue(response.is_error(), "Should not be able to change email without authentication")

        # Check error code 403 and error message "User must be a student"
        self.assertEqual(response.error.error_code, 403, "Should return a 403 error")
        self.assertEqual(response.error.error_message, "User must be a student",
                         "Should return 'User must be a student'")

        self.assertEqual(len(self.event_bus.events), 0, "Should not be triggered an event")


if __name__ == '__main__':
    unittest.main()
