import unittest
from unittest.mock import Mock
from datetime import datetime

from madissues_backend.core.issues.domain.issue_mother import IssueMother
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.issues.application.commands.comments.toggle_like_issue_comment_command import (
    ToggleLikeIssueCommentCommand,
    LikeCommentRequest,
    LikeCommentResponse
)
from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_repository import MockIssueCommentRepository
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service


class TestToggleLikeIssueCommentCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")

        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)

        # Create issueComment created by the student
        self.issue_comment = IssueMother.random_issue_comment()
        self.issue_comment.likes = []
        self.issue_comment.author = self.student.id

        self.issue_comment_repository = MockIssueCommentRepository(self.db)
        self.issue_comment_repository.add(
            self.issue_comment
        )
        self.command = ToggleLikeIssueCommentCommand(
            authentication_service=self.authentication_service,
            issue_comment_repository=self.issue_comment_repository
        )

    def test_like_comment_successfully(self):
        user_id = str(GenericUUID.next_id())
        request = LikeCommentRequest(
            comment_id=str(self.issue_comment.id),
            user_id=user_id
        )

        response = self.command.run(request)
        self.assertTrue(response.is_success(), "The response should be successful")
        self.assertEqual(response.success.id, str(self.issue_comment.id), "The liked comment ID should be returned")
        self.assertEqual(response.success.likes_count, 1, "The likes count should be incremented")

    def test_unlike_comment_successfully(self):
        user_id = str(GenericUUID.next_id())
        self.issue_comment.likes.append(GenericUUID(user_id))
        self.issue_comment_repository.save(self.issue_comment)

        request = LikeCommentRequest(
            comment_id=str(self.issue_comment.id),
            user_id=user_id
        )

        response = self.command.run(request)
        self.assertTrue(response.is_success(), "The response should be successful")
        self.assertEqual(response.success.id, str(self.issue_comment.id), "The liked comment ID should be returned")
        self.assertEqual(response.success.likes_count, 0, "The likes count should be decremented")

    def test_like_nonexistent_comment(self):
        user_id = str(GenericUUID.next_id())
        request = LikeCommentRequest(
            comment_id=str(GenericUUID.next_id()),
            user_id=user_id
        )

        response = self.command.run(request)
        self.assertFalse(response.is_success(), "The response should not be successful")
        self.assertEqual(response.error.error_message, "Comment not found")


if __name__ == '__main__':
    unittest.main()
