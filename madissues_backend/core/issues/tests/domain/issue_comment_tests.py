import unittest
from datetime import datetime
from pydantic import ValidationError

from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestIssueComment(unittest.TestCase):
    def setUp(self):
        self.valid_comment_data = {
            'id': GenericUUID.next_id(),
            'issue_id': GenericUUID.next_id(),
            'author': GenericUUID.next_id(),
            'likes': [GenericUUID.next_id()],
            'content': 'Test comment content',
            'timestamp': datetime.now(),
            'response_to': None
        }

    def test_valid_comment(self):
        comment = IssueComment(**self.valid_comment_data)
        self.assertIsInstance(comment, IssueComment)

    def test_missing_issue_id(self):
        invalid_comment_data = self.valid_comment_data.copy()
        del invalid_comment_data['issue_id']
        with self.assertRaises(ValidationError):
            IssueComment(**invalid_comment_data)

    def test_missing_author(self):
        invalid_comment_data = self.valid_comment_data.copy()
        del invalid_comment_data['author']
        with self.assertRaises(ValidationError):
            IssueComment(**invalid_comment_data)

    def test_missing_likes(self):
        invalid_comment_data = self.valid_comment_data.copy()
        del invalid_comment_data['likes']
        with self.assertRaises(ValidationError):
            IssueComment(**invalid_comment_data)

    def test_missing_content(self):
        invalid_comment_data = self.valid_comment_data.copy()
        del invalid_comment_data['content']
        with self.assertRaises(ValidationError):
            IssueComment(**invalid_comment_data)

    def test_missing_timestamp(self):
        invalid_comment_data = self.valid_comment_data.copy()
        del invalid_comment_data['timestamp']
        with self.assertRaises(ValidationError):
            IssueComment(**invalid_comment_data)

    def test_invalid_response_to(self):
        invalid_comment_data = self.valid_comment_data.copy()
        invalid_comment_data['response_to'] = 'invalid_uuid'
        with self.assertRaises(ValidationError):
            IssueComment(**invalid_comment_data)

    def test_response_to(self):
        valid_response_to = GenericUUID.next_id()
        valid_comment_data = self.valid_comment_data.copy()
        valid_comment_data['response_to'] = valid_response_to
        comment = IssueComment(**valid_comment_data)
        self.assertEqual(comment.response_to, valid_response_to)


if __name__ == '__main__':
    unittest.main()
