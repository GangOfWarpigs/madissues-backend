import unittest

from madissues_backend.core.issues.domain.issue_mother import IssueMother
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestMockIssueRepository(unittest.TestCase):
    def setUp(self):
        self.entity_table = EntityTable()
        self.repo = MockIssueRepository(self.entity_table)
        # Create 10 random issues saving them to a list
        self.added_issues = [IssueMother.random_issue() for _ in range(10)]
        # Add the issues to the repository
        for issue in self.added_issues:
            self.repo.add(issue)

    def test_add_issue(self):
        new_issue = IssueMother.random_issue()
        self.repo.add(new_issue)
        self.assertIn(new_issue.id, self.repo._issues)

    def test_save_existing_issue(self):
        issue = next(iter(self.added_issues))
        issue.details = "Updated details"
        saved_issue = self.repo.save(issue)
        self.assertEqual(saved_issue.details, "Updated details")

    def test_save_non_existing_issue(self):
        non_existing_issue = IssueMother.random_issue()
        with self.assertRaises(ValueError):
            self.repo.save(non_existing_issue)

    def test_remove_existing_issue(self):
        issue_id = next(iter(self.added_issues)).id
        self.repo.remove(issue_id)
        self.assertNotIn(issue_id, self.repo._issues)

    def test_remove_non_existing_issue(self):
        non_existing_id = GenericUUID.next_id()
        with self.assertRaises(ValueError):
            self.repo.remove(non_existing_id)

    def test_get_by_id(self):
        issue = next(iter(self.added_issues))
        fetched_issue = self.repo.get_by_id(issue.id)
        self.assertEqual(fetched_issue, issue)

    def test_get_by_non_existing_id(self):
        non_existing_id = GenericUUID.next_id()
        fetched_issue = self.repo.get_by_id(non_existing_id)
        self.assertIsNone(fetched_issue)

    def test_get_all(self):
        all_issues = self.repo.get_all()
        self.assertEqual(len(all_issues), len(self.repo._issues))

    def test_get_all_by_status(self):
        status = "In progress"
        issues_by_status = self.repo.get_all_by_status(status)
        self.assertTrue(all(issue.status == status for issue in issues_by_status))

    def test_get_all_by_course(self):
        course_id = next(iter(self.added_issues)).course
        issues_by_course = self.repo.get_all_by_course(course_id)
        self.assertTrue(all(issue.course == course_id for issue in issues_by_course))

    def test_get_all_by_teacher(self):
        teacher_id = next(iter(self.added_issues)).teachers[0]
        issues_by_teacher = self.repo.get_all_by_teacher(teacher_id)
        self.assertTrue(all(teacher_id in issue.teachers for issue in issues_by_teacher))



if __name__ == '__main__':
    unittest.main()
