import unittest

from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.issues.domain.issue_mother import IssueMother


class MyTestCase(unittest.TestCase):
    def test_create_1000_issues(self):
        for _ in range(1000):
            issue = IssueMother.random_issue()
            self.assertIsInstance(issue, Issue)

    def test_create_1000_issue_comments(self):
        for _ in range(1000):
            issue_comment = IssueMother.random_issue_comment()
            self.assertIsInstance(issue_comment, IssueComment)


if __name__ == '__main__':
    unittest.main()
