import unittest

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.students.application.commands.update_student_preferences_command import \
    UpdateStudentPreferencesCommand, ChangeStudentPreferencesRequest
from madissues_backend.core.students.domain.student_mother import StudentMother
from madissues_backend.core.students.infrastructure.mocks.mock_student_repository import MockStudentRepository


class TestUpdateStudentPreferencesCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.student_repository = MockStudentRepository(self.db)
        self.event_bus = MockEventBus()
        self.student = StudentMother.random_student()
        self.student_repository.add(self.student)

    def tearDown(self):
        self.event_bus.events = []

    def test_change_student_preferences_successful(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Initialize authentication service with a valid student token
        authentication_service = create_mock_authentication_service(self.db)(self.student.token)

        # Initialize command
        command = UpdateStudentPreferencesCommand(authentication_service, self.student_repository, self.event_bus)

        # Create request
        request = ChangeStudentPreferencesRequest(
            language="en",
            theme="Dark"
        )

        # Execute the command with the request
        response = command.execute(request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Preferences should be updated")
        self.assertEqual(response.success.student_id, str(self.student.id), "Response should contain student_id")
        self.assertEqual(self.student_repository.get_by_id(self.student.id).preferences.language, "en",
                         "Language should be updated in db")
        self.assertEqual(self.student_repository.get_by_id(self.student.id).preferences.theme, "Dark",
                         "Theme should be updated in db")
        self.assertEqual(len(self.event_bus.events), 1, "Should trigger an event")

    def test_change_student_preferences_unauthenticated(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Initialize authentication service with an invalid token
        authentication_service = create_mock_authentication_service(self.db)("invalid_token")

        # Initialize command
        command = UpdateStudentPreferencesCommand(authentication_service, self.student_repository, self.event_bus)

        # Create request
        request = ChangeStudentPreferencesRequest(
            language="en",
            theme="Dark"
        )

        # Execute the command with the request
        response = command.execute(request)

        # Assert error and check response data
        self.assertTrue(response.is_error(), "Should not be able to change preferences without authentication")

        # Check error code 403 and error message "User must be a student"
        self.assertEqual(response.error.error_code, 403, "Should return a 403 error")
        self.assertEqual(response.error.error_message, "User must be a student",
                         "Should return 'User must be a student'")

        self.assertEqual(len(self.event_bus.events), 0, "Should not be triggered an event")


if __name__ == '__main__':
    unittest.main()
