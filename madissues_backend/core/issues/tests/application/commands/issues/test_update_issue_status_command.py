import unittest

from madissues_backend.core.issues.application.commands.issues.update_issue_status_command import (
    UpdateIssueStatusCommand,
    UpdateIssueStatusRequest
)
from madissues_backend.core.issues.domain.issue_mother import IssueMother
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus


class TestUpdateIssueStatusCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.issue_repository = MockIssueRepository(self.db)
        self.event_bus = MockEventBus()
        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        self.command = UpdateIssueStatusCommand(
            authentication_service=self.authentication_service,
            issue_repository=self.issue_repository,
            event_bus=self.event_bus
        )

        # Create issue created by the student
        self.issue = IssueMother.random_issue()
        self.issue.student_id = self.student.id

        self.issue_repository.add(self.issue)

    def test_update_issue_status_successfully(self):
        new_status = "Solved"
        request = UpdateIssueStatusRequest(
            issue_id=str(self.issue.id),
            user_id=str(self.issue.student_id),
            new_status=new_status
        )

        response = self.command.run(request)
        self.assertTrue(response.is_success())
        self.assertEqual(response.success.id, str(self.issue.id))
        self.assertEqual(response.success.new_status, new_status)

    def test_update_issue_status_unauthorized(self):
        new_status = "Solved"
        unauthorized_user_id = str(GenericUUID.next_id())
        request = UpdateIssueStatusRequest(
            issue_id=str(self.issue.id),
            user_id=unauthorized_user_id,
            new_status=new_status
        )

        response = self.command.run(request)
        self.assertFalse(response.is_success())
        self.assertIn("Unauthorized", response.error.error_message)

    def test_update_nonexistent_issue(self):
        new_status = "Solved"
        request = UpdateIssueStatusRequest(
            issue_id=str(GenericUUID.next_id()),  # Nonexistent issue ID
            user_id=str(self.issue.student_id),
            new_status=new_status
        )

        response = self.command.run(request)
        self.assertFalse(response.is_success())
        self.assertIn("Issue not found", response.error.error_message)


if __name__ == '__main__':
    unittest.main()
