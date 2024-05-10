import unittest

from madissues_backend.core.organizations.application.commands.teacher.create_organization_teacher_command import \
    CreateOrganizationTeacherRequest, CreateOrganizationTeacherResponse, CreateOrganizationTeacherCommand
from madissues_backend.core.organizations.application.commands.teacher.delete_organization_teacher_command import \
    DeleteOrganizationTeacherRequest, DeleteOrganizationTeacherResponse, DeleteOrganizationTeacherCommand
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus


class TestDeleteOrganizationTeacherCommand(unittest.TestCase):
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
        teacher_request = CreateOrganizationTeacherRequest(
            organization_id=str(self.organization.id),
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            office_link="https://www.dis.ulpgc.es/john-doe",
            courses=[str(course_id) for course_id in self.organization.courses]
        )
        create_command = CreateOrganizationTeacherCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        create_response = create_command.execute(teacher_request)
        teacher_id = create_response.success.id

        # Reset event bus
        self.event_bus.events = []

        delete_request = DeleteOrganizationTeacherRequest(
            teacher_id=teacher_id,
            organization_id=str(self.organization.id)
        )
        delete_command = DeleteOrganizationTeacherCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = delete_command.execute(delete_request)

        # Assert
        self.assertTrue(response.is_success(), "Teacher should be deleted successfully")
        self.assertEqual(response.success.teacher_id, teacher_id,
                         "ID of deleted teacher should match the requested teacher ID")
        self.assertEqual(response.success.organization_id, str(self.organization.id),
                         "Organization ID should match the requested organization ID")
        self.assertEqual(len(self.event_bus.events), 1, "Should be triggered an event")

    def test_execute_invalid_organization_teacher_id(self):
        # Arrange
        delete_request = DeleteOrganizationTeacherRequest(
            teacher_id="invalid_id",
            organization_id=str(self.organization.id)
        )
        delete_command = DeleteOrganizationTeacherCommand(
            authentication_service=self.authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act
        response = delete_command.execute(delete_request)

        # Assert
        self.assertTrue(not response.success, "Teacher ID should be invalid")
        self.assertEqual(response.error.error_message, "Invalid teacher ID",
                         "Should return 'Invalid teacher ID'")

    def test_execute_unauthorized(self):
        # Arrange
        unauthorized_owner = self.db.tables['owners'][GenericUUID("ca7b384c-0ae9-489f-90c6-a18a6781dcd0")]
        authentication_service = create_mock_authentication_service(self.db)(unauthorized_owner.token)
        delete_request = DeleteOrganizationTeacherRequest(
            teacher_id=str(GenericUUID("f1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b")),
            organization_id=str(self.organization.id)
        )
        delete_command = DeleteOrganizationTeacherCommand(
            authentication_service=authentication_service,
            repository=self.organization_repository,
            event_bus=self.event_bus
        )

        # Act (raises an exception)
        response = delete_command.execute(delete_request)

        # Assert
        self.assertTrue(not response.success, "User should not be authorized")
        self.assertEqual(response.error.error_message, "You are not the owner of the organization",
                         "Should return 'You are not the owner of the organization'")


if __name__ == '__main__':
    unittest.main()
