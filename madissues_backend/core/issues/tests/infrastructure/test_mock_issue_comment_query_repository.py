import unittest
from datetime import datetime
from random import Random

from madissues_backend.core.issues.domain.issue_mother import IssueMother
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_query_repository import \
    MockIssueCommentQueryRepository
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_repository import MockIssueCommentRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestMockIssueCommentRepository(unittest.TestCase):
    def setUp(self):
        self.entity_table = EntityTable()
        self.query_repo = MockIssueCommentQueryRepository(self.entity_table)
        self.repo = MockIssueCommentRepository(self.entity_table)
        # Create 10 random issue comments saving them to a list
        self.added_comments = [IssueMother.random_issue_comment(issue_id=GenericUUID.next_id(),
                                                                author=GenericUUID.next_id(),
                                                                response_to=GenericUUID.next_id())
                               for _ in range(10)]
        # Add the issue comments to the repository
        for comment in self.added_comments:
            self.repo.add(comment)

            # Create random
        self.rand = Random()

    def test_get_all(self):
        all_comments = self.query_repo.get_all()
        self.assertEqual(len(all_comments), len(self.query_repo._issue_comments))

    def test_get_all_by_author(self):
        author_id = self.rand.choice(self.added_comments).author
        comments_by_author = self.query_repo.get_all_by_author(author_id)
        self.assertTrue(all(comment.author == str(author_id) for comment in comments_by_author))

    def test_get_all_by_issue(self):
        issue_id = self.rand.choice(self.added_comments).issue_id
        comments_by_issue = self.query_repo.get_all_by_issue(issue_id)
        self.assertTrue(all(comment.issue_id == str(issue_id) for comment in comments_by_issue))

    def test_get_all_by_response_to(self):
        response_to_id = self.rand.choice(self.added_comments).response_to
        comments_by_response_to = self.query_repo.get_all_by_response_to(response_to_id)
        self.assertTrue(all(comment.response_to == str(response_to_id) for comment in comments_by_response_to))

    def test_get_all_by_date_greater_than(self):
        date = datetime(self.rand.randint(1990, 2100), self.rand.randint(1, 12), self.rand.randint(1, 28))
        comments_after_date = self.query_repo.get_all_by_date_greater_than(date)
        self.assertTrue(all(datetime.strptime(comment.date_time, "%Y-%m-%d") > date for comment in comments_after_date))

    def test_get_all_by_date_less_than(self):
        # Random date between 2023 - 2025
        date = datetime(self.rand.randint(1990, 2100), self.rand.randint(1, 12), self.rand.randint(1, 28))
        comments_before_date = self.query_repo.get_all_by_date_less_than(date)
        self.assertTrue(all(datetime.strptime(comment.date_time, "%Y-%m-%d") < date for comment in comments_before_date))

    def test_get_by_id_nonexistent(self):
        retrieved_comment = self.query_repo.get_by_id(GenericUUID.next_id())
        self.assertIsNone(retrieved_comment)

    def test_get_all_by_author_nonexistent(self):
        retrieved_comments = self.query_repo.get_all_by_author(GenericUUID.next_id())
        self.assertEqual(len(retrieved_comments), 0)

    def test_get_all_by_issue_nonexistent(self):
        retrieved_comments = self.query_repo.get_all_by_issue(GenericUUID.next_id())
        self.assertEqual(len(retrieved_comments), 0)

    def test_get_all_by_response_to_nonexistent(self):
        retrieved_comments = self.query_repo.get_all_by_response_to(GenericUUID.next_id())
        self.assertEqual(len(retrieved_comments), 0)

    def test_get_all_by_date_greater_than_nonexistent(self):
        retrieved_comments = self.query_repo.get_all_by_date_greater_than(self.added_comments[-1].date_time)
        # Find number of comments with date greater than the last comment's date
        num_comments = len(
            [comment for comment in self.added_comments if comment.date_time > self.added_comments[-1].date_time])
        self.assertEqual(len(retrieved_comments), num_comments)

    def test_get_all_by_date_less_than_nonexistent(self):
        retrieved_comments = self.query_repo.get_all_by_date_less_than(self.added_comments[-1].date_time)
        # Find number of comments with date less than the last comment's date
        num_comments = len(
            [comment for comment in self.added_comments if comment.date_time < self.added_comments[-1].date_time])
        self.assertEqual(len(retrieved_comments), num_comments)


if __name__ == '__main__':
    unittest.main()
