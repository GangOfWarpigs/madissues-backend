import time
import unittest

from madissues_backend.core.issues.application.commands.issues.create_issue_command import CreateIssueCommand, \
    CreateIssueRequest
from madissues_backend.core.issues.application.commands.issues.update_issue_information_command import \
    UpdateIssueInformationRequest, UpdateIssueInformationCommand
from madissues_backend.core.issues.domain.issue_mother import IssueMother
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import (
    create_mock_authentication_service,
)
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService


class TestUpdateIssueInfoCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.issue_repository = MockIssueRepository(self.db)
        self.event_bus = MockEventBus()
        self.organization = self.db.tables["organizations"][GenericUUID("cc164174-07f7-4cd4-8a7e-43c96d9b825a")]
        self.owner = self.db.tables['owners'][GenericUUID("83d150fe-84f4-4a22-a109-5704342c589c")]
        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        self.storage_service = LocalStorageService("../../../../../../media")

        self.command = UpdateIssueInformationCommand(
            authentication_service=self.authentication_service,
            issue_repository=self.issue_repository,
            storage_service=self.storage_service,
            event_bus=self.event_bus
        )

        # Create issue created by the student
        self.issue = IssueMother.random_issue()
        self.issue.proofs = [
            "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"
        ]
        self.issue.student_id = self.student.id
        # Create a new issue
        create_response = CreateIssueCommand(
            authentication_service=self.authentication_service,
            repository=self.issue_repository,
            storage_service=self.storage_service,
            event_bus=self.event_bus
        ).execute(
            CreateIssueRequest(
                title=self.issue.title,
                description=self.issue.description,
                details=self.issue.details,
                proofs=self.issue.proofs,
                course=str(self.issue.course),
                teachers=[str(teacher) for teacher in self.issue.teachers],
                organization_id=str(self.organization.id)
            )
        )

        assert create_response.is_success(), "The response to the issue creation should be successful"

        # Assign the id to the issue
        self.issue.id = GenericUUID(create_response.success.id)

        # Reset the event bus
        self.event_bus.events = []

    def tearDown(self):
        try:
            self.storage_service.clear_folder("issues")
        except Exception as e:
            pass


    def test_update_issue_information_successfully(self):
        # Setup request with valid updates
        request = UpdateIssueInformationRequest(
            issue_id=str(self.issue.id),
            title="Updated Title",
            description="Updated Description",
            details="Updated Details",
            proofs=[],
            teachers=[str(GenericUUID.next_id())]
        )

        response = self.command.run(request)

        self.assertTrue(response.is_success())
        updated_issue = self.issue_repository.get_by_id(self.issue.id)

        self.assertEqual(updated_issue.title, "Updated Title")
        self.assertEqual(updated_issue.description, "Updated Description")
        self.assertEqual(updated_issue.details, "Updated Details")
        # Assert triggered events
        self.assertEqual(len(self.event_bus.events), 1)

    def test_unauthorized_update_attempt(self):
        # Change the author of the issue
        self.issue.student_id = GenericUUID.next_id()
        self.issue_repository.save(self.issue)

        request = UpdateIssueInformationRequest(
            issue_id=str(self.issue.id),
            title="Updated Title",
            description="Updated Description",
            details="Updated Details",
            proofs=["iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
                    "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"],
            teachers=[str(GenericUUID.next_id())]
        )

        response = self.command.run(request)
        self.assertFalse(response.is_success())
        self.assertEqual(response.error.error_message, "Unauthorized to update this issue")

    def test_update_nonexistent_issue(self):
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        request = UpdateIssueInformationRequest(
            issue_id=str(GenericUUID.next_id()),  # Nonexistent issue
            title="Updated Title",
            description="Updated Description",
            details="Updated Details",
            proofs=["iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
                    "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"],
            teachers=[str(GenericUUID.next_id())]
        )

        response = self.command.run(request)
        self.assertFalse(response.is_success())
        self.assertIn("Issue not found", response.error.error_message)


if __name__ == "__main__":
    unittest.main()
