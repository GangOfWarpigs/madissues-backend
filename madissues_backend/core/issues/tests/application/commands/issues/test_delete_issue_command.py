import unittest
from unittest.mock import Mock

from madissues_backend.core.issues.application.commands.issues.delete_issue_command import (
    DeleteIssueCommand,
    DeleteIssueRequest,
    DeleteIssueResponse
)
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.domain.issue_mother import IssueMother
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.domain.response import Response


class TestDeleteIssueCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.issue_repository = MockIssueRepository(self.db)
        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        self.command = DeleteIssueCommand(
            authentication_service=self.authentication_service,
            issue_repository=self.issue_repository
        )

        # Create issue created by the student
        self.issue = IssueMother.random_issue()
        self.issue.student_id = self.student.id

        self.issue_repository.add(self.issue)

    def test_delete_issue_successfully(self):
        request = DeleteIssueRequest(
            issue_id=str(self.issue.id),
            user_id=str(self.issue.student_id)
        )
        self.authentication_service.get_user_id = Mock(return_value=str(self.issue.student_id))

        response = self.command.run(request)
        self.assertTrue(response.is_success(), "The response should be successful")
        self.assertEqual(response.success.id, str(self.issue.id))

    def test_delete_issue_unauthorized(self):
        unauthorized_user_id = str(GenericUUID.next_id())
        request = DeleteIssueRequest(
            issue_id=str(self.issue.id),
            user_id=unauthorized_user_id
        )
        self.authentication_service.get_user_id = Mock(return_value=unauthorized_user_id)

        response = self.command.run(request)
        self.assertFalse(response.is_success(), "The response should not be successful")
        self.assertIn("Unauthorized", response.error.error_message)

    def test_delete_nonexistent_issue(self):
        request = DeleteIssueRequest(
            issue_id=str(GenericUUID.next_id()),  # Nonexistent issue ID
            user_id=str(self.issue.student_id)
        )
        self.issue_repository.get_by_id = Mock(return_value=None)

        response = self.command.run(request)
        self.assertFalse(response.is_success(), "The response should not be successful")
        self.assertIn("Issue not found", response.error.error_message)

    def test_delete_issue_as_site_admin(self):
        # Change the author of the issue
        self.issue.student_id = GenericUUID.next_id()

        # Make the student a site admin
        self.student.is_site_admin = True

        request = DeleteIssueRequest(
            issue_id=str(self.issue.id),
            user_id=str(self.student.id)
        )

        response = self.command.run(request)
        self.assertTrue(response.is_success(), "The response should be successful")
        self.assertEqual(response.success.id, str(self.issue.id))


if __name__ == '__main__':
    unittest.main()
