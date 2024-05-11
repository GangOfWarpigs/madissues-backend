import unittest
from unittest.mock import Mock
from datetime import datetime

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.issues.application.commands.comments.change_issue_comment_command import (
    ChangeIssueCommentCommand,
    ChangeCommentRequest,
    ChangeCommentResponse
)
from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_repository import MockIssueCommentRepository
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service


class TestChangeIssueCommentCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")

        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)

        # Create issueComment created by the student
        self.issue_comment = IssueComment(
            id=GenericUUID.next_id(),
            issue_id=GenericUUID.next_id(),
            author=self.student.id,
            content="Original content",
            date_time=datetime.now(),
            likes=[],
            response_to=None
        )
        self.issue_comment_repository = MockIssueCommentRepository(self.db)
        self.issue_comment_repository.add(self.issue_comment)

        self.command = ChangeIssueCommentCommand(
            authentication_service=self.authentication_service,
            issue_comment_repository=self.issue_comment_repository
        )

    def test_change_comment_successfully(self):
        new_content = "Updated content"
        request = ChangeCommentRequest(
            comment_id=str(self.issue_comment.id),
            user_id=str(self.student.id),
            new_content=new_content
        )

        response = self.command.execute(request)
        self.assertTrue(response.is_success())
        self.assertEqual(response.success.id, str(self.issue_comment.id))
        self.assertEqual(response.success.new_content, new_content)
        self.assertIsNotNone(response.success.updated_date_time)

    def test_change_comment_unauthorized(self):
        new_content = "Attempted unauthorized update"
        another_student_id = str(GenericUUID.next_id())  # Another student who is not the author
        request = ChangeCommentRequest(
            comment_id=str(self.issue_comment.id),
            user_id=another_student_id,
            new_content=new_content
        )

        response = self.command.execute(request)
        self.assertFalse(response.is_success())
        self.assertEqual(response.error.error_code, 401)
        self.assertEqual(response.error.error_message, "Unauthorized. You are not the author of the comment")

    def test_change_nonexistent_comment(self):
        new_content = "Updated content"
        request = ChangeCommentRequest(
            comment_id=str(GenericUUID.next_id()),  # Nonexistent comment ID
            user_id=str(self.student.id),
            new_content=new_content
        )
        self.issue_comment_repository.get_by_id = Mock(return_value=None)  # Simulate non-existence

        response = self.command.execute(request)
        self.assertFalse(response.is_success())
        self.assertEqual(response.error.error_code, 404)
        self.assertEqual(response.error.error_message, "Comment not found")


if __name__ == '__main__':
    unittest.main()
