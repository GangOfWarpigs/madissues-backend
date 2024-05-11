import unittest
from unittest.mock import Mock
from datetime import datetime

from madissues_backend.core.issues.domain.issue_mother import IssueMother
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.issues.application.commands.comments.delete_issue_comment_command import \
    DeleteCommentCommand, \
    DeleteCommentRequest
from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_repository import MockIssueCommentRepository
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service


class TestDeleteCommentCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")

        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)

        # Create issueComment created by the student
        self.issue_comment = IssueMother.random_issue_comment()
        self.issue_comment.author = self.student.id

        self.issue_comment_repository = MockIssueCommentRepository(self.db)
        self.issue_comment_repository.add(
            self.issue_comment
        )

        self.command = DeleteCommentCommand(
            authentication_service=self.authentication_service,
            issue_comment_repository=self.issue_comment_repository
        )

    def test_delete_comment_successfully(self):
        comment_id = str(self.issue_comment.id)
        author_id = str(self.issue_comment.author)
        request = DeleteCommentRequest(
            comment_id=comment_id,
            author_id=author_id
        )

        response = self.command.run(request)
        self.assertTrue(response.is_success(), "The response should be successful")
        self.assertEqual(response.success.id, comment_id, "The deleted comment ID should be returned")

    def test_delete_comment_unauthorized(self):
        comment_id = str(GenericUUID.next_id())
        author_id = str(GenericUUID.next_id())
        request = DeleteCommentRequest(
            comment_id=comment_id,
            author_id=author_id
        )

        self.authentication_service.get_user_id = Mock(return_value="another_user_id")
        response = self.command.run(request)
        self.assertFalse(response.is_success(), "The response should not be successful")
        self.assertTrue(response.is_error(), "The operation should fail due to authorization")

    def test_delete_nonexistent_comment(self):
        comment_id = str(GenericUUID.next_id())
        author_id = str(GenericUUID.next_id())
        request = DeleteCommentRequest(
            comment_id=comment_id,
            author_id=author_id
        )

        self.issue_comment_repository.get_by_id = Mock(return_value=None)
        response = self.command.run(request)
        self.assertFalse(response.is_success(), "The response should not be successful")
        self.assertTrue(response.is_error(), "The operation should fail due to nonexistent comment")

    def test_delete_comment_authorized_site_admin(self):
        # Generate new random comment
        new_issue_comment = IssueMother.random_issue_comment()

        assert new_issue_comment.author is not self.student.id, \
            "The author of the comment should not be the student"

        # Make the student a site admin
        self.student.is_site_admin = True

        # Add the new comment to the repository
        self.issue_comment_repository.add(
            new_issue_comment
        )

        comment_id = str(new_issue_comment.id)
        author_id = str(new_issue_comment.author)
        request = DeleteCommentRequest(
            comment_id=comment_id,
            author_id=author_id
        )
        response = self.command.run(request)

        self.assertTrue(response.is_success(), "The response should be successful")
        self.assertEqual(response.success.id, comment_id, "The deleted comment ID should be returned")


if __name__ == '__main__':
    unittest.main()
