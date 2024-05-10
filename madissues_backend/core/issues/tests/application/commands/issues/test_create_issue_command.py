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


class TestCreateIssueCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_issues")
        self.event_bus = MockEventBus()
        self.authorization_service = create_mock_authentication_service(self.db)
        self.authorization = self.authorization_service("1d372590-a034-4e05-b1e8-02a9e91068f3")
        self.issue_repository = MockIssueRepository(self.db)
        self.storage_service = MockStorageService()

    def test_issue_is_created_without_errors(self):
        command = CreateIssueCommand(
            self.authorization_service, self.issue_repository, self.event_bus
        )
        response = command.execute(
            CreateIssueRequest(
                title="issue1",
                description="Description of issue1",
                details="Details of issue1",
                proofs=["proof1.jpg", "proof2.jpg"],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID("course1")),
                teachers=[str(GenericUUID("teacher1")), str(GenericUUID("teacher2"))],
                student=str(GenericUUID("student1")),
            )
        )

        assert response.is_success() is True, "Command must succeed"
        assert response.success.title == "issue1"
        assert self.issue_repository.get_by_id(GenericUUID(response.success.id)) is not None

    def test_issue_is_created_with_invalid_status(self):
        command = CreateIssueCommand(
            self.authorization_service, self.issue_repository, self.event_bus
        )
        response = command.execute(
            CreateIssueRequest(
                title="issue1",
                description="Description of issue1",
                details="Details of issue1",
                proofs=["proof1.jpg", "proof2.jpg"],
                status="InvalidStatus",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID("course1")),
                teachers=[str(GenericUUID("teacher1")), str(GenericUUID("teacher2"))],
                student=str(GenericUUID("student1")),
            )
        )

        assert response.is_error() is True, "Command must fail"
        assert response.error.error_code == 1, "Error code must be caused by invalid status"
        self.assertIn("status", response.error.error_field, "Must be caused by status")

    def test_issue_is_created_with_empty_title(self):
        command = CreateIssueCommand(
            self.authorization_service, self.issue_repository, self.event_bus
        )
        response = command.execute(
            CreateIssueRequest(
                title="",
                description="Description of issue1",
                details="Details of issue1",
                proofs=["proof1.jpg", "proof2.jpg"],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID("course1")),
                teachers=[str(GenericUUID("teacher1")), str(GenericUUID("teacher2"))],
                student=str(GenericUUID("student1")),
            )
        )

        assert response.is_error() is True, "Command must fail"
        assert response.error.error_code == 1, "Error code must be caused by empty title"
        self.assertIn("title", response.error.error_field, "Must be caused by title")

    def test_issue_is_created_with_empty_description(self):
        command = CreateIssueCommand(
            self.authorization_service, self.issue_repository, self.event_bus
        )
        response = command.execute(
            CreateIssueRequest(
                title="issue1",
                description="",
                details="Details of issue1",
                proofs=["proof1.jpg", "proof2.jpg"],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID("course1")),
                teachers=[str(GenericUUID("teacher1")), str(GenericUUID("teacher2"))],
                student=str(GenericUUID("student1")),
            )
        )

        assert response.is_error() is True, "Command must fail"
        assert response.error.error_code == 1, "Error code must be caused by empty description"
        self.assertIn("description", response.error.error_field, "Must be caused by description")

    def test_issue_is_created_with_empty_proofs(self):
        command = CreateIssueCommand(
            self.authorization_service, self.issue_repository, self.event_bus
        )
        response = command.execute(
            CreateIssueRequest(
                title="issue1",
                description="Description of issue1",
                details="Details of issue1",
                proofs=[],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID("course1")),
                teachers=[str(GenericUUID("teacher1")), str(GenericUUID("teacher2"))],
                student=str(GenericUUID("student1")),
            )
        )

        assert response.is_success() is True, "Command must succeed"
        assert len(response.success.proofs) == 0, "Proofs must be empty"

    def test_issue_is_created_with_invalid_student_id(self):
        command = CreateIssueCommand(
            self.authorization_service, self.issue_repository, self.event_bus
        )
        response = command.execute(
            CreateIssueRequest(
                title="issue1",
                description="Description of issue1",
                details="Details of issue1",
                proofs=["proof1.jpg", "proof2.jpg"],
                status="Queued",
                date_time=datetime.now().strftime("%Y-%m-%d"),
                course=str(GenericUUID("course1")),
                teachers=[str(GenericUUID("teacher1")), str(GenericUUID("teacher2"))],
                student="invalid_student_id",
            )
        )

        assert response.is_error() is True, "Command must fail"
        assert response.error.error_code == 1, "Error code must be caused by invalid student ID"
        self.assertIn("student", response.error.error_field, "Must be caused by student ID")


if __name__ == "__main__":
    unittest.main()
