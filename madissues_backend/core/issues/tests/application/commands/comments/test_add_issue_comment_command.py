import unittest
from datetime import datetime

from madissues_backend.core.issues.application.commands.comments.add_comment_to_issue import AddCommentToIssueCommand, \
    AddCommentToIssueRequest
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_repository import MockIssueCommentRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service


class TestAddCommentToIssueCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        self.issue_comment_repository = MockIssueCommentRepository(self.db)
        self.command = AddCommentToIssueCommand(
            authentication_service=self.authentication_service,
            issue_comment_repository=self.issue_comment_repository
        )

    def test_add_comment_to_issue_successfully(self):
        issue_id = str(GenericUUID.next_id())
        author_id = str(GenericUUID.next_id())
        content = "This is a test comment"
        request = AddCommentToIssueRequest(
            issue_id=issue_id,
            author_id=author_id,
            content=content
        )

        response = self.command.run(request)
        self.assertTrue(response.is_success(), "The response should be successful")
        self.assertEqual(response.success.issue_id, issue_id)
        self.assertEqual(response.success.author_id, author_id)
        self.assertEqual(response.success.content, content)
        self.assertEqual(response.success.date_time, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.assertIsNotNone(response.success.id, "A new UUID should be assigned to the comment")

    def test_add_comment_to_issue_with_invalid_author(self):
        issue_id = str(GenericUUID.next_id())
        author_id = "invalid_uuid"  # This should be validated by your AuthenticationService
        content = "This is a test comment"
        request = AddCommentToIssueRequest(
            issue_id=issue_id,
            author_id=author_id,
            content=content
        )

        response = self.command.run(request)
        self.assertFalse(response.is_success(), "The response should not be successful")
        self.assertIsNotNone(response.error, "Should return an error for invalid author")

    def test_add_comment_to_nonexistent_issue(self):
        issue_id = str(GenericUUID.next_id())
        author_id = str(GenericUUID.next_id())
        content = "This is a test comment"
        request = AddCommentToIssueRequest(
            issue_id="nonexistent_issue_id",  # This should ideally trigger a not found error in the repository
            author_id=author_id,
            content=content
        )

        response = self.command.run(request)
        self.assertFalse(response.is_success(), "The response should not be successful")
        self.assertIsNotNone(response.error, "Should return an error for nonexistent issue")

    def test_add_empty_content_comment(self):
        issue_id = str(GenericUUID.next_id())
        author_id = str(GenericUUID.next_id())
        content = ""  # This should be handled as invalid input
        request = AddCommentToIssueRequest(
            issue_id=issue_id,
            author_id=author_id,
            content=content
        )

        response = self.command.run(request)
        self.assertFalse(response.is_success(), "The response should not be successful")
        self.assertIsNotNone(response.error, "Should return an error for empty content")

    def test_add_comment_to_issue_with_response_to_id(self):
        issue_id = str(GenericUUID.next_id())
        author_id = str(GenericUUID.next_id())
        content = "This is a test comment"
        response_to_id = str(GenericUUID.next_id())
        request = AddCommentToIssueRequest(
            issue_id=issue_id,
            author_id=author_id,
            content=content,
            response_to_id=response_to_id
        )

        response = self.command.run(request)
        self.assertTrue(response.is_success(), "The response should be successful")
        self.assertEqual(response.success.issue_id, issue_id)
        self.assertEqual(response.success.author_id, author_id)
        self.assertEqual(response.success.content, content)
        self.assertIsNotNone(response.success.id, "A new UUID should be assigned to the comment")
        self.assertEqual(response.success.response_to_id, response_to_id)


if __name__ == '__main__':
    unittest.main()
