import unittest
from datetime import datetime, timedelta

from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_query_repository import MockIssueQueryRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestMockIssueQueryRepository(unittest.TestCase):
    def setUp(self):
        self.entity_table = EntityTable()
        self.repo = MockIssueQueryRepository(self.entity_table)
        organization_id = GenericUUID.next_id()
        # Create 10 random issues saving them to a list
        self.added_issues = [Issue(
            id=GenericUUID.next_id(),
            title=f"Title {i}",
            description=f"Description {i}",
            details=f"Details {i}",
            proofs=[f"Proof {i}.png" for i in range(3)],
            status="Queued",
            date_time=datetime.now(),
            course=GenericUUID.next_id(),
            teachers=[GenericUUID.next_id()],
            student_id=GenericUUID.next_id(),
            organization_id=organization_id
        ) for i in range(10)]
        # Add the issues to the repository
        for issue in self.added_issues:
            self.repo.db.tables["issues"][issue.id] = issue

    def test_get_all_by_organization(self):
        organization_id = str(self.added_issues[0].organization_id)
        result = self.repo.get_all_by_organization(organization_id)
        self.assertEqual(len(result), len(self.added_issues))

    def test_get_by_id(self):
        issue_id = str(self.added_issues[0].id)
        result = self.repo.get_by_id(issue_id)
        self.assertIsNotNone(result)

    def test_get_all_by_title(self):
        title = self.added_issues[0].title
        result = self.repo.get_all_by_title(title)
        self.assertEqual(len(result), 1)

    def test_get_all_by_course(self):
        course_id = str(self.added_issues[0].course)
        result = self.repo.get_all_by_course(course_id)
        self.assertEqual(len(result), 1)

    def test_get_all_by_student(self):
        student_id = str(self.added_issues[0].student_id)
        result = self.repo.get_all_by_student(student_id)
        self.assertEqual(len(result), 1)

    def test_get_all_by_teacher(self):
        teacher_id = str(self.added_issues[0].teachers[0])
        result = self.repo.get_all_by_teacher(teacher_id)
        self.assertEqual(len(result), 1)

    def test_get_all_by_status(self):
        status = self.added_issues[0].status
        result = self.repo.get_all_by_status(status)
        self.assertEqual(len(result), 10)

    def test_get_all(self):
        result = self.repo.get_all()
        self.assertEqual(len(result), len(self.added_issues))

    def test_get_all_by_date_greater_than(self):
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        result = self.repo.get_all_by_date_greater_than(date)
        self.assertEqual(len(result), len(self.added_issues))

    def test_get_all_by_date_less_than(self):
        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        result = self.repo.get_all_by_date_less_than(date)
        self.assertEqual(len(result), len(self.added_issues))


if __name__ == '__main__':
    unittest.main()
