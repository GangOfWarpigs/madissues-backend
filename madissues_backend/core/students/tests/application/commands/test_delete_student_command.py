import unittest

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.students.application.commands.delete_student_account_command import DeleteStudentCommand, \
    DeleteStudentRequest
from madissues_backend.core.students.domain.student_mother import StudentMother
from madissues_backend.core.students.infrastructure.mocks.mock_student_repository import MockStudentRepository


class TestDeleteStudentCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.student_repository = MockStudentRepository(self.db)
        self.event_bus = MockEventBus()
        self.student_being_deleted = StudentMother.random_student()
        self.student_being_deleted.is_council_member = False
        self.student_being_deleted.is_site_admin = False

        self.council_member = StudentMother.random_student()
        self.council_member.is_council_member = True

        self.site_admin = StudentMother.random_student()
        self.site_admin.is_site_admin = True

        self.unauthorized_student = StudentMother.random_student()
        self.unauthorized_student.is_council_member = False
        self.unauthorized_student.is_site_admin = False

        # Add student to repository
        self.student_repository.add(self.student_being_deleted)
        self.student_repository.add(self.council_member)
        self.student_repository.add(self.site_admin)
        self.student_repository.add(self.unauthorized_student)

    def test_delete_student_successful_as_council_member(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Initialize authentication service with a valid council member token (get class and instantiate)
        authentication_service = create_mock_authentication_service(self.db)(self.council_member.token)
        command = DeleteStudentCommand(authentication_service, self.student_repository, self.event_bus)
        request = DeleteStudentRequest(
            student_id=str(self.student_being_deleted.id)
        )

        # Execute the command with the request
        response = command.execute(request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Student should be deleted")
        self.assertEqual(response.success.student_id, str(self.student_being_deleted.id),
                         "Response should contain student_id")
        # Check if student is deleted from repository
        with self.assertRaises(ValueError):
            self.student_repository.get_by_id(self.student_being_deleted.id)

        self.assertEqual(len(self.event_bus.events), 1, "Should be triggered an event")

    def test_delete_student_successful_as_site_admin(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Initialize authentication service with a valid site admin token (get class and instantiate)
        authentication_service = create_mock_authentication_service(self.db)(self.site_admin.token)
        command = DeleteStudentCommand(authentication_service, self.student_repository, self.event_bus)
        request = DeleteStudentRequest(
            student_id=str(self.student_being_deleted.id)
        )

        # Execute the command with the request
        response = command.execute(request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Student should be deleted")
        self.assertEqual(response.success.student_id, str(self.student_being_deleted.id),
                         "Response should contain student_id")
        # Check if student is deleted from repository
        with self.assertRaises(ValueError):
            self.student_repository.get_by_id(self.student_being_deleted.id)

        self.assertEqual(len(self.event_bus.events), 1, "Should be triggered an event")

    def test_delete_student_unauthenticated(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Initialize authentication service with an unauthorized student token (get class and instantiate)
        authentication_service = create_mock_authentication_service(self.db)(self.unauthorized_student.token)
        command = DeleteStudentCommand(authentication_service, self.student_repository, self.event_bus)
        request = DeleteStudentRequest(
            student_id=str(self.student_being_deleted.id)
        )

        # Execute the command with the request
        response = command.execute(request)

        # Assert error and check response data
        self.assertTrue(response.is_error(), "Should not be able to delete student without proper permissions")

        # Check error code 500 and error message "You can only delete your own account"
        self.assertEqual(response.error.error_code, 500, "Should return a 500 error")
        self.assertEqual(response.error.error_message, "You can only delete your own account",
                         "Should return 'You can only delete your own account'")

        self.assertEqual(len(self.event_bus.events), 0, "Should not be triggered an event")


if __name__ == '__main__':
    unittest.main()
