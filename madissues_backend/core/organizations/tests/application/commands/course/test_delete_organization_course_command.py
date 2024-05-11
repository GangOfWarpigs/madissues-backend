import unittest

from madissues_backend.core.organizations.application.commands.course.delete_organization_course_command import \
    DeleteOrganizationCourseRequest, DeleteOrganizationCourseResponse, DeleteOrganizationCourseCommand
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus


class TestDeleteOrganizationCourseCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.organization_repository = MockOrganizationRepository(self.db)
        self.event_bus = MockEventBus()
        self.event_bus.events = []
        self.organization_id = GenericUUID("cc164174-07f7-4cd4-8a7e-43c96d9b825a")
        self.owner = self.db.tables['owners'][GenericUUID("83d150fe-84f4-4a22-a109-5704342c589c")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.owner.token)

    # Cleanup function
    def tearDown(self):
        self.event_bus.events = []

    def test_execute_success(self):
        # Arrange
        course_id = "2b3d1324-346b-40cb-9b7f-f744fe06b59d"
        request = DeleteOrganizationCourseRequest(
            course_id=course_id,
            organization_id=str(self.organization_id)
        )
        command = DeleteOrganizationCourseCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(request)

        # Assert
        self.assertTrue(response.is_success(), "Course should be deleted")
        self.assertEqual(response.success.course_id, course_id,
                         "Correct course ID should be returned in response")
        self.assertEqual(response.success.organization_id, str(self.organization_id),
                         "Correct organization ID should be returned in response")
        self.assertEqual(len(self.event_bus.events), 1, "Should be triggered an event")

    def test_execute_invalid_organization_id(self):
        # Arrange
        course_id = "2b3d1324-346b-40cb-9b7f-f744fe06b59d"
        request = DeleteOrganizationCourseRequest(
            course_id=course_id,
            organization_id="invalid_id"
        )
        command = DeleteOrganizationCourseCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(request)

        # Assert
        self.assertTrue(not response.success, "Organization ID should be invalid")
        self.assertEqual(response.error.error_message, "Invalid organization ID",
                         "Should return 'Invalid organization ID'")

    def test_execute_unauthorized(self):
        # Arrange
        course_id = "2b3d1324-346b-40cb-9b7f-f744fe06b59d"
        unauthorized_owner = self.db.tables['owners'][GenericUUID("ca7b384c-0ae9-489f-90c6-a18a6781dcd0")]
        authentication_service = create_mock_authentication_service(self.db)(unauthorized_owner.token)
        request = DeleteOrganizationCourseRequest(
            course_id=course_id,
            organization_id=str(self.organization_id)
        )
        command = DeleteOrganizationCourseCommand(
            authentication_service=authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act (raises an exception)
        response = command.execute(request)

        # Assert
        self.assertTrue(not response.success, "User should not be authorized")
        self.assertEqual(response.error.error_message, "You are not the owner of the organization",
                         "Should return 'User must be an owner of the organization'")


if __name__ == '__main__':
    unittest.main()
