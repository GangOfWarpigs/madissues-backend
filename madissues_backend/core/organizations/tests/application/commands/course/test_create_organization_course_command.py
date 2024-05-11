import unittest

from madissues_backend.core.organizations.application.commands.course.create_organization_course_command import \
    CreateOrganizationCourseRequest, CreateOrganizationCourseResponse, CreateOrganizationCourseCommand
from madissues_backend.core.organizations.domain.organization_mother import OrganizationMother
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus


class TestCreateOrganizationCourseCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.organization_repository = MockOrganizationRepository(self.db)
        self.event_bus = MockEventBus()
        self.organization = self.organization_repository.get_by_id(GenericUUID("cc164174-07f7-4cd4-8a7e-43c96d9b825a"))
        self.owner = self.db.tables['owners'][GenericUUID("83d150fe-84f4-4a22-a109-5704342c589c")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.owner.token)

    def tearDown(self):
        self.event_bus.events = []

    def test_execute_success(self):
        # Arrange
        course_request = CreateOrganizationCourseRequest(
            organization_id=str(self.organization.id),
            name="Mathematics",
            code="MATHS101",
            icon="math_icon.png",
            primary_color="#ffffff",
            secondary_color="#000000"
        )
        command = CreateOrganizationCourseCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(course_request)

        # Assert
        self.assertTrue(response.is_success(), "Course should be created successfully")
        self.assertIsNotNone(response.success.id, "Course ID should not be None")
        self.assertEqual(response.success.organization_id, course_request.organization_id,
                         "Organization ID should match")
        self.assertEqual(response.success.name, course_request.name, "Course name should match")
        self.assertEqual(response.success.code, course_request.code, "Course code should match")
        self.assertEqual(response.success.icon, course_request.icon, "Course icon should match")
        self.assertEqual(response.success.primary_color, course_request.primary_color,
                         "Course primary color should match")
        self.assertEqual(response.success.secondary_color, course_request.secondary_color,
                         "Course secondary color should match")

        # Course should be added to the organization
        organization = self.organization_repository.get_by_id(GenericUUID(course_request.organization_id))
        self.assertTrue((GenericUUID(response.success.id) in [course.id for course in organization.courses]),
                        "Course should be added to the organization")
        self.assertEqual(len(self.event_bus.events), 1, "Should trigger an event")

    def test_execute_invalid_organization_id(self):
        # Arrange
        course_request = CreateOrganizationCourseRequest(
            organization_id="invalid_id",
            name="Mathematics",
            code="MATH101",
            icon="math_icon.png",
            primary_color="#ffffff",
            secondary_color="#000000"
        )
        command = CreateOrganizationCourseCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(course_request)

        # Assert
        self.assertTrue(not response.success, "Organization ID should be invalid")
        self.assertEqual(response.error.error_message, "Invalid organization ID",
                         "Should return 'Invalid organization ID'")

    def test_execute_unauthorized(self):
        # Arrange
        unauthorized_owner = self.db.tables['owners'][GenericUUID("ca7b384c-0ae9-489f-90c6-a18a6781dcd0")]
        authentication_service = create_mock_authentication_service(self.db)(unauthorized_owner.token)
        course_request = CreateOrganizationCourseRequest(
            organization_id=str(self.organization.id),
            name="Mathematics",
            code="MATH101",
            icon="math_icon.png",
            primary_color="#ffffff",
            secondary_color="#000000"
        )
        command = CreateOrganizationCourseCommand(
            authentication_service=authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act (raises an exception)
        response = command.execute(course_request)

        # Assert
        self.assertTrue(not response.success, "User should not be authorized")
        self.assertEqual(response.error.error_message, "You are not the owner of the organization",
                         "Should return 'User must be an owner of the organization'")


if __name__ == '__main__':
    unittest.main()
