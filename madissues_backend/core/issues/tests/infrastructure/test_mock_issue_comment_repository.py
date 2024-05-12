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


if __name__ == '__main__':
    unittest.main()
