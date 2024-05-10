import unittest
from datetime import datetime

from madissues_backend.core.issues.application.commands.issues.create_issue_command import \
    CreateIssueCommand, CreateIssueRequest
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService


class TestCreateIssueCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_student_created")
        self.event_bus = MockEventBus()
        self.storage_service = LocalStorageService("../../../../../../media")
        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        self.issue_repository = MockIssueRepository(self.db)

    def test_create_issue_without_proofs(self):
        # Create issue without proofs
        create_command = CreateIssueCommand(self.authentication_service,
                                            self.issue_repository,
                                            self.event_bus,
                                            self.storage_service)

        create_response = create_command.run(CreateIssueRequest(
            title="Test Issue",
            description="Description of the test issue",
            details="Additional details",
            proofs=[],
            status="Queued",
            date_time=datetime.now().strftime('%Y-%m-%d'),
            course="c0517ecb-24e5-4d5e-841c-48b7001e5f94",
            teachers=["d93ab3a5-7cb0-4a23-9327-ae15c2481675"],
            student="1d372590-a034-4e05-b1e8-02a9e91068f3"
        ))

        assert create_response.is_success() is True, "Issue must be created successfully"
        assert create_response.success.title == "Test Issue", "Title must match"
        assert create_response.success.description == "Description of the test issue", "Description must match"
        assert create_response.success.details == "Additional details", "Details must match"
        assert create_response.success.status == "Queued", "Status must match"

    def test_create_issue_with_proofs(self):
        # Create issue with proofs
        create_command = CreateIssueCommand(self.authentication_service,
                                            self.issue_repository,
                                            self.event_bus,
                                            self.storage_service)

        proofs_base64 = [
            "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA"
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
            student="1d372590-a034-4e05-b1e8-02a9e91068f3"
        ))

        assert create_response.is_success() is True, "Issue must be created successfully"
        assert create_response.success.title == "Test Issue", "Title must match"
        assert create_response.success.description == "Description of the test issue", "Description must match"
        assert create_response.success.details == "Additional details", "Details must match"
        assert create_response.success.status == "Queued", "Status must match"
        assert len(create_response.success.proofs) == 2, "Proofs must be added"

    def test_create_issue_unauthorized_user(self):
        unauthorized_token = "fa68b53a-8db6-4f5b-9d15-e93cbc163bf0"
        self.authentication_service = create_mock_authentication_service(self.db)(unauthorized_token)
        # Create issue with unauthorized user
        create_command = CreateIssueCommand(self.authentication_service,
                                            self.issue_repository,
                                            self.event_bus,
                                            self.storage_service)

        create_response = create_command.run(CreateIssueRequest(
            title="Test Issue",
            description="Description of the test issue",
            details="Additional details",
            proofs=[],
            status="Queued",
            date_time=datetime.now().strftime('%Y-%m-%d'),
            course="c0517ecb-24e5-4d5e-841c-48b7001e5f94",
            teachers=["d93ab3a5-7cb0-4a23-9327-ae15c2481675"],
            student="ca7b384c-0ae9-489f-90c6-a18a6781dcd0"
        ))

        assert create_response.is_error() is True, "Issue creation must fail"
        assert create_response.error.error_code == 403, "Error code must indicate 'forbidden'"
        assert create_response.error.error_message == "User must be a student", "Error message must indicate 'forbidden'"
