import unittest
from datetime import datetime
from pydantic import ValidationError
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestIssue(unittest.TestCase):
    def setUp(self):
        self.valid_issue_data = {
            'id': GenericUUID.next_id(),
            'title': 'Test Issue',
            'description': 'Test description',
            'details': 'Test details',
            'proofs': ['https://example.com/image1.jpg', 'https://example.com/image2.png'],
            'status': 'Queued',
            'date_time': datetime.now(),
            'course': GenericUUID.next_id(),
            'teachers': [GenericUUID.next_id(), GenericUUID.next_id()],
            'student': GenericUUID.next_id(),
            'task_manager_id': GenericUUID.next_id(),
            'assigned_to': GenericUUID.next_id()
        }

    def test_valid_issue(self):
        issue = Issue(**self.valid_issue_data)
        self.assertIsInstance(issue, Issue)

    def test_missing_title(self):
        invalid_issue_data = self.valid_issue_data.copy()
        del invalid_issue_data['title']
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_missing_description(self):
        invalid_issue_data = self.valid_issue_data.copy()
        del invalid_issue_data['description']
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_invalid_status(self):
        invalid_issue_data = self.valid_issue_data.copy()
        invalid_issue_data['status'] = 'InvalidStatus'
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_missing_date_time(self):
        invalid_issue_data = self.valid_issue_data.copy()
        del invalid_issue_data['date_time']
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_invalid_proofs(self):
        invalid_issue_data = self.valid_issue_data.copy()
        invalid_issue_data['proofs'] = ['invalid_link']
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_missing_course(self):
        invalid_issue_data = self.valid_issue_data.copy()
        del invalid_issue_data['course']
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_missing_assigned_to(self):
        invalid_issue_data = self.valid_issue_data.copy()
        del invalid_issue_data['assigned_to']
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_invalid_teacher_list(self):
        invalid_issue_data = self.valid_issue_data.copy()
        invalid_issue_data['teachers'] = 'invalid_teacher_list'
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_invalid_student_id(self):
        invalid_issue_data = self.valid_issue_data.copy()
        invalid_issue_data['student'] = 'invalid_student_id'
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_missing_details(self):
        invalid_issue_data = self.valid_issue_data.copy()
        del invalid_issue_data['details']
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)

    def test_invalid_task_manager_id(self):
        invalid_issue_data = self.valid_issue_data.copy()
        invalid_issue_data['task_manager_id'] = 'invalid_task_manager_id'
        with self.assertRaises(ValidationError):
            Issue(**invalid_issue_data)


if __name__ == '__main__':
    unittest.main()
