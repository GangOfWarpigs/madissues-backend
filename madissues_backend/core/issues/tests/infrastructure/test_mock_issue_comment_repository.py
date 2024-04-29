import unittest

from madissues_backend.core.issues.domain.issue_mother import IssueMother
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_repository import MockIssueCommentRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestMockIssueCommentRepository(unittest.TestCase):
    def setUp(self):
        self.entity_table = EntityTable()
        self.repo = MockIssueCommentRepository(self.entity_table)
        # Create 10 random issue comments saving them to a list
        self.added_comments = [IssueMother.random_issue_comment(issue_id=GenericUUID.next_id(),
                                                                author=GenericUUID.next_id())
                               for _ in range(10)]
        # Add the issue comments to the repository
        for comment in self.added_comments:
            self.repo.add(comment)

    def test_add_issue_comment(self):
        new_comment = IssueMother.random_issue_comment(issue_id=GenericUUID.next_id(),
                                                       author=GenericUUID.next_id())
        self.repo.add(new_comment)
        self.assertIn(new_comment.id, self.repo._issues)

    def test_save_existing_issue_comment(self):
        comment = next(iter(self.added_comments))
        comment.content = "Updated text"
        self.repo.save(comment)
        saved_comment = self.repo.get_by_id(comment.id)
        self.assertEqual(saved_comment.content, "Updated text")

    def test_save_non_existing_issue_comment(self):
        non_existing_comment = IssueMother.random_issue_comment(issue_id=GenericUUID.next_id(),
                                                                author=GenericUUID.next_id())
        with self.assertRaises(ValueError):
            self.repo.save(non_existing_comment)

    def test_remove_existing_issue_comment(self):
        comment_id = next(iter(self.added_comments)).id
        self.repo.remove(comment_id)
        self.assertNotIn(comment_id, self.repo._issues)

    def test_remove_non_existing_issue_comment(self):
        non_existing_id = GenericUUID.next_id()
        with self.assertRaises(ValueError):
            self.repo.remove(non_existing_id)

    def test_get_by_id(self):
        comment = next(iter(self.added_comments))
        fetched_comment = self.repo.get_by_id(comment.id)
        self.assertEqual(fetched_comment, comment)

    def test_get_all(self):
        all_comments = self.repo.get_all()
        self.assertEqual(len(all_comments), len(self.repo._issues))

    def test_get_all_by_author(self):
        author_id = next(iter(self.added_comments)).author
        comments_by_author = self.repo.get_all_by_author(author_id)
        self.assertTrue(all(comment.author == author_id for comment in comments_by_author))

    def test_get_all_by_issue(self):
        issue_id = next(iter(self.added_comments)).issue_id
        comments_by_issue = self.repo.get_all_by_issue(issue_id)
        self.assertTrue(all(comment.issue_id == issue_id for comment in comments_by_issue))

    def test_get_all_by_response_to(self):
        response_to_id = next(iter(self.added_comments)).response_to
        comments_by_response_to = self.repo.get_all_by_response_to(response_to_id)
        self.assertTrue(all(comment.response_to == response_to_id for comment in comments_by_response_to))

    def test_get_all_by_date_greater_than(self):
        date = next(iter(self.added_comments)).date_time
        comments_after_date = self.repo.get_all_by_date_greater_than(date)
        self.assertTrue(all(comment.date_time > date for comment in comments_after_date))

    def test_get_all_by_date_less_than(self):
        date = next(iter(self.added_comments)).date_time
        comments_before_date = self.repo.get_all_by_date_less_than(date)
        self.assertTrue(all(comment.date_time < date for comment in comments_before_date))

    def test_get_by_id_nonexistent(self):
        retrieved_comment = self.repo.get_by_id(GenericUUID.next_id())
        self.assertIsNone(retrieved_comment)

    def test_save_nonexistent_issue_comment(self):
        non_existing_comment = IssueMother.random_issue_comment(issue_id=GenericUUID.next_id(),
                                                                author=GenericUUID.next_id())
        with self.assertRaises(ValueError):
            self.repo.save(non_existing_comment)

    def test_remove_nonexistent_issue_comment(self):
        with self.assertRaises(ValueError):
            self.repo.remove(GenericUUID.next_id())

    def test_get_all_by_author_nonexistent(self):
        retrieved_comments = self.repo.get_all_by_author(GenericUUID.next_id())
        self.assertEqual(len(retrieved_comments), 0)

    def test_get_all_by_issue_nonexistent(self):
        retrieved_comments = self.repo.get_all_by_issue(GenericUUID.next_id())
        self.assertEqual(len(retrieved_comments), 0)

    def test_get_all_by_response_to_nonexistent(self):
        retrieved_comments = self.repo.get_all_by_response_to(GenericUUID.next_id())
        self.assertEqual(len(retrieved_comments), 0)

    def test_get_all_by_date_greater_than_nonexistent(self):
        retrieved_comments = self.repo.get_all_by_date_greater_than(self.added_comments[-1].date_time)
        # Find number of comments with date greater than the last comment's date
        num_comments = len([comment for comment in self.added_comments if comment.date_time > self.added_comments[-1].date_time])
        self.assertEqual(len(retrieved_comments), num_comments)

    def test_get_all_by_date_less_than_nonexistent(self):
        retrieved_comments = self.repo.get_all_by_date_less_than(self.added_comments[-1].date_time)
        # Find number of comments with date less than the last comment's date
        num_comments = len([comment for comment in self.added_comments if comment.date_time < self.added_comments[-1].date_time])
        self.assertEqual(len(retrieved_comments), num_comments)




if __name__ == '__main__':
    unittest.main()
