import unittest

from madissues_backend.core.organizations.application.commands.course.update_organization_course_command import \
    UpdateOrganizationCourseRequest, UpdateOrganizationCourseResponse, UpdateOrganizationCourseCommand
from madissues_backend.core.organizations.domain.organization_mother import OrganizationMother
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus


class TestUpdateOrganizationCourseCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.organization_repository = MockOrganizationRepository(self.db)
        self.event_bus = MockEventBus()
        self.organization = self.organization_repository.get_by_id(GenericUUID("cc164174-07f7-4cd4-8a7e-43c96d9b825a"))
        self.owner = self.db.tables['owners'][GenericUUID("83d150fe-84f4-4a22-a109-5704342c589c")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.owner.token)

    def test_execute_success(self):
        # Arrange
        course = OrganizationMother.generate_organization_course()
        self.organization.courses.append(course)
        updated_name = "Updated Course Name"
        updated_code = "UCN101"
        updated_icon = "updated-icon.png"
        updated_primary_color = "#FFFFFF"
        updated_secondary_color = "#000000"

        course_request = UpdateOrganizationCourseRequest(
            course_id=str(course.id),
            organization_id=str(self.organization.id),
            name=updated_name,
            code=updated_code,
            icon=updated_icon,
            primary_color=updated_primary_color,
            secondary_color=updated_secondary_color
        )

        command = UpdateOrganizationCourseCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(course_request)

        # Assert
        self.assertTrue(response.is_success(), "Response should indicate success")
        self.assertEqual(len(self.event_bus.events), 1, "Should be triggered an event")
        self.assertEqual(response.success.course_id, str(course.id), "Course ID should match")
        self.assertEqual(response.success.organization_id, str(self.organization.id), "Organization ID should match")
        self.assertEqual(response.success.name, updated_name, "Name should be updated")
        self.assertEqual(response.success.code, updated_code, "Code should be updated")
        self.assertEqual(response.success.icon, updated_icon, "Icon should be updated")
        self.assertEqual(response.success.primary_color, updated_primary_color, "Primary color should be updated")
        self.assertEqual(response.success.secondary_color, updated_secondary_color, "Secondary color should be updated")

    def test_execute_invalid_organization_id(self):
        # Arrange
        course = OrganizationMother.generate_organization_course()
        self.organization.courses.append(course)
        updated_name = "Updated Course Name"
        updated_code = "UCN101"
        updated_icon = "updated-icon.png"
        updated_primary_color = "#FFFFFF"
        updated_secondary_color = "#000000"

        course_request = UpdateOrganizationCourseRequest(
            course_id=str(course.id),
            organization_id="invalid_id",
            name=updated_name,
            code=updated_code,
            icon=updated_icon,
            primary_color=updated_primary_color,
            secondary_color=updated_secondary_color
        )

        command = UpdateOrganizationCourseCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(course_request)

        # Assert
        self.assertTrue(not response.success, "Organization ID should be invalid")
        self.assertEqual(len(self.event_bus.events), 0, "Should not be triggered any event")
        self.assertEqual(response.error.error_message, "Invalid organization ID", "Error message should match")

    def test_execute_unauthorized(self):
        # Reset events
        self.event_bus.events = []

        # Arrange
        unauthorized_owner = self.db.tables['owners'][GenericUUID("ca7b384c-0ae9-489f-90c6-a18a6781dcd0")]
        authentication_service = create_mock_authentication_service(self.db)(unauthorized_owner.token)

        course = OrganizationMother.generate_organization_course()
        self.organization.courses.append(course)
        updated_name = "Updated Course Name"
        updated_code = "UCN101"
        updated_icon = "updated-icon.png"
        updated_primary_color = "#FFFFFF"
        updated_secondary_color = "#000000"

        course_request = UpdateOrganizationCourseRequest(
            course_id=str(course.id),
            organization_id=str(self.organization.id),
            name=updated_name,
            code=updated_code,
            icon=updated_icon,
            primary_color=updated_primary_color,
            secondary_color=updated_secondary_color
        )

        command = UpdateOrganizationCourseCommand(
            authentication_service=authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = command.execute(course_request)

        # Assert
        self.assertTrue(not response.success, "User should not be authorized")
        self.assertEqual(len(self.event_bus.events), 0, "Should not be triggered any event")
        self.assertEqual(response.error.error_message, "You are not the owner of the organization",
                         "Error message should match")


if __name__ == '__main__':
    unittest.main()
