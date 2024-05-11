import unittest
from datetime import datetime

from madissues_backend.core.issues.application.commands.issues.create_issue_command import (
    CreateIssueCommand,
    CreateIssueRequest,
)
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import (
    create_mock_authentication_service,
)
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.mocks.mock_storage_service import MockStorageService
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService


class TestCreateIssueCommand(unittest.TestCase):
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

    def test_issue_is_created_without_errors(self):
        # Reset event bus
        self.event_bus.events = []
        command = CreateIssueCommand(
            self.authentication_service,
            self.issue_repository,
            self.storage_service,
            self.event_bus
        )

        response = command.run(
            CreateIssueRequest(
                title="issue1",
                description="Description of issue1",
                details="Details of issue1",
                proofs=["iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
                        "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID.next_id()),
                teachers=[str(GenericUUID.next_id()), str(GenericUUID.next_id())],
                student=str(self.student.id),
                organization_id=str(self.organization.id)
            )
        )

        assert response.is_success() is True, "Command must succeed"
        assert response.success.title == "issue1"
        assert response.success.description == "Description of issue1"
        assert response.success.details == "Details of issue1"
        assert response.success.status == "Queued"
        self.assertEqual(len(response.success.proofs), 2)
        self.assertEqual(len(response.success.teachers), 2)
        self.assertEqual(response.success.student, str(self.student.id))
        self.assertEqual(response.success.organization_id, str(self.organization.id))

        # Assert one event triggered
        assert len(self.event_bus.events) == 1
        assert self.issue_repository.get_by_id(GenericUUID(response.success.id)) is not None

    def test_issue_is_created_with_invalid_status(self):
        # Reset event bus
        self.event_bus.events = []
        command = CreateIssueCommand(
            self.authentication_service, self.issue_repository,
            self.storage_service, self.event_bus
        )
        response = command.run(
            CreateIssueRequest(
                title="issue1",
                description="Description of issue1",
                details="Details of issue1",
                proofs=["iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
                        "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"],
                status="InvalidStatus",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID.next_id()),
                teachers=[str(GenericUUID.next_id()), str(GenericUUID.next_id())],
                student=str(self.student.id),
                organization_id=str(self.organization.id)
            )
        )

        assert response.is_error() is True, "Command must fail"
        assert response.error.error_code == 1, "Error code must be caused by invalid status"
        self.assertIn("status", response.error.error_field, "Must be caused by status")

    def test_issue_is_created_with_empty_title(self):
        # Reset event bus
        self.event_bus.events = []
        command = CreateIssueCommand(
            self.authentication_service, self.issue_repository,
            self.storage_service,
            self.event_bus
        )
        response = command.run(
            CreateIssueRequest(
                title="",
                description="Description of issue1",
                details="Details of issue1",
                proofs=["iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
                        "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID.next_id()),
                teachers=[str(GenericUUID.next_id()), str(GenericUUID.next_id())],
                student=str(self.student.id),
                organization_id=str(self.organization.id)
            )
        )

        assert response.is_error() is True, "Command must fail"
        assert response.error.error_code == 1, "Error code must be caused by empty title"
        self.assertIn("title", response.error.error_field, "Must be caused by title")

    def test_issue_is_created_with_empty_description(self):
        # Reset event bus
        self.event_bus.events = []
        command = CreateIssueCommand(
            self.authentication_service, self.issue_repository,
            self.storage_service,
            self.event_bus
        )
        response = command.run(
            CreateIssueRequest(
                title="issue1",
                description="",
                details="Details of issue1",
                proofs=["iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
                        "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID.next_id()),
                teachers=[str(GenericUUID.next_id()), str(GenericUUID.next_id())],
                student=str(self.student.id),
                organization_id=str(self.organization.id)
            )
        )

        assert response.is_error() is True, "Command must fail"
        assert response.error.error_code == 1, "Error code must be caused by empty description"
        self.assertIn("description", response.error.error_field, "Must be caused by description")

    def test_issue_is_created_with_empty_proofs(self):
        # Reset event bus
        self.event_bus.events = []
        command = CreateIssueCommand(
            self.authentication_service, self.issue_repository,
            self.storage_service,
            self.event_bus
        )
        response = command.run(
            CreateIssueRequest(
                title="issue1",
                description="Description of issue1",
                details="Details of issue1",
                proofs=[],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID.next_id()),
                teachers=[str(GenericUUID.next_id()), str(GenericUUID.next_id())],
                student=str(self.student.id),
                organization_id=str(self.organization.id)
            )
        )

        assert response.is_success() is True, "Command must succeed"
        assert len(response.success.proofs) == 0, "Proofs must be empty"

    def test_issue_is_created_with_invalid_student_id(self):
        # Reset event bus
        self.event_bus.events = []
        command = CreateIssueCommand(
            self.authentication_service, self.issue_repository,
            self.storage_service,
            self.event_bus
        )
        response = command.run(
            CreateIssueRequest(
                title="issue1",
                description="Description of issue1",
                details="Details of issue1",
                proofs=["iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
                        "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID.next_id()),
                teachers=[str(GenericUUID.next_id()), str(GenericUUID.next_id())],
                student=str("invalid_id"),
                organization_id=str(self.organization.id),
            )
        )

        assert response.is_error() is True, "Command must fail"
        # Assert no events triggered
        assert len(self.event_bus.events) == 0

    def test_create_issue_without_proofs(self):
        # Reset event bus
        self.event_bus.events = []
        # Create issue without proofs
        create_command = CreateIssueCommand(self.authentication_service,
                                            self.issue_repository,
                                            self.storage_service,
                                            self.event_bus)

        create_response = create_command.run(CreateIssueRequest(
            title="Test Issue",
            description="Description of the test issue",
            details="Additional details",
            proofs=[],
            status="Queued",
            date_time=datetime.now().strftime('%Y-%m-%d'),
            course="c0517ecb-24e5-4d5e-841c-48b7001e5f94",
            teachers=["d93ab3a5-7cb0-4a23-9327-ae15c2481675"],
            student="1d372590-a034-4e05-b1e8-02a9e91068f3",
            organization_id="fa68b53a-8db6-4f5b-9d15-e93cbc163bfa"
        ))

        assert create_response.is_success() is True, "Issue must be created successfully"
        assert create_response.success.title == "Test Issue", "Title must match"
        assert create_response.success.description == "Description of the test issue", "Description must match"
        assert create_response.success.details == "Additional details", "Details must match"
        assert create_response.success.status == "Queued", "Status must match"

    def test_create_issue_with_proofs_with_commas(self):
        # Reset event bus
        self.event_bus.events = []
        # Create issue with proofs
        create_command = CreateIssueCommand(self.authentication_service,
                                            self.issue_repository,
                                            self.storage_service,
                                            self.event_bus)

        proofs_base64 = [
            ",iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            ",iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"
        ]

        create_response = create_command.run(CreateIssueRequest(
            title="Test Issue",
            description="Description of the test issue",
            details="Additional details",
            proofs=proofs_base64,
            status="Queued",
            date_time=datetime.now().strftime('%Y-%m-%d'),
            course="c0517ecb-24e5-4d5e-841c-48b7001e5f94",
            teachers=["d93ab3a5-7cb0-4a23-9327-ae15c2481675"],
            student="1d372590-a034-4e05-b1e8-02a9e91068f3",
            organization_id="fa68b53a-8db6-4f5b-9d15-e93cbc163bfa"
        ))

        assert create_response.is_success() is True, "Issue must be created successfully"
        assert create_response.success.title == "Test Issue", "Title must match"
        assert create_response.success.description == "Description of the test issue", "Description must match"
        assert create_response.success.details == "Additional details", "Details must match"
        assert create_response.success.status == "Queued", "Status must match"
        assert len(create_response.success.proofs) == 2, "Proofs must be added"

    def test_create_issue_unauthorized_user(self):
        # Reset event bus
        self.event_bus.events = []
        unauthorized_token = "fa68b53a-8db6-4f5b-9d15-e93cbc163bf0"
        self.authentication_service = create_mock_authentication_service(self.db)(unauthorized_token)
        # Create issue with unauthorized user
        create_command = CreateIssueCommand(self.authentication_service,
                                            self.issue_repository,
                                            self.storage_service,
                                            self.event_bus)

        create_response = create_command.run(CreateIssueRequest(
            title="Test Issue",
            description="Description of the test issue",
            details="Additional details",
            proofs=[],
            status="Queued",
            date_time=datetime.now().strftime('%Y-%m-%d'),
            course="c0517ecb-24e5-4d5e-841c-48b7001e5f94",
            teachers=["d93ab3a5-7cb0-4a23-9327-ae15c2481675"],
            student="ca7b384c-0ae9-489f-90c6-a18a6781dcd0",
            organization_id="fa68b53a-8db6-4f5b-9d15-e93cbc163bfa"
        ))

        assert create_response.is_error() is True, "Issue creation must fail"
        assert create_response.error.error_code == 403, "Error code must indicate 'forbidden'"
        assert create_response.error.error_message == "User must be a student", "Error message must indicate 'forbidden'"


if __name__ == "__main__":
    unittest.main()
