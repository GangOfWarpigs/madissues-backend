import unittest
from datetime import datetime

from pydantic import ValidationError

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.domain.student import Student
from madissues_backend.core.students.domain.student_preferences import StudentPreferences
from madissues_backend.core.students.domain.student_profile import StudentProfile


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.valid_student_data = {
            'id': GenericUUID.next_id(),
            'organization_id': GenericUUID.next_id(),
            'email': 'tests@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'TestPassword123',
            'started_studies_date': datetime.now(),
            'is_site_admin': False,
            'is_council_member': True,
            'is_banned': False,
            'token': 'test_token',
            'profile': StudentProfile(
                degree=GenericUUID.next_id(),
                joined_courses=[GenericUUID.next_id(), GenericUUID.next_id()]
            ),
            'preferences': StudentPreferences(
                language='en',
                theme='Light'
            )
        }

    def test_valid_student(self):
        student = Student(**self.valid_student_data)
        self.assertIsInstance(student, Student)

    def test_missing_organization(self):
        invalid_student_data = self.valid_student_data.copy()
        del invalid_student_data['organization_id']
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)

    def test_missing_email(self):
        invalid_student_data = self.valid_student_data.copy()
        del invalid_student_data['email']
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)

    def test_invalid_email(self):
        invalid_student_data = self.valid_student_data.copy()
        invalid_student_data['email'] = 'invalid_email'
        with self.assertRaises(ValueError):
            Student(**invalid_student_data)

    def test_missing_first_name(self):
        invalid_student_data = self.valid_student_data.copy()
        del invalid_student_data['first_name']
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)

    def test_missing_last_name(self):
        invalid_student_data = self.valid_student_data.copy()
        del invalid_student_data['last_name']
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)

    def test_missing_started_studies_date(self):
        invalid_student_data = self.valid_student_data.copy()
        del invalid_student_data['started_studies_date']
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)

    def test_invalid_started_studies_date(self):
        invalid_student_data = self.valid_student_data.copy()
        invalid_student_data['started_studies_date'] = 'invalid_date'
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)

    def test_missing_is_site_admin(self):
        invalid_student_data = self.valid_student_data.copy()
        del invalid_student_data['is_site_admin']
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)

    def test_missing_is_council_member(self):
        invalid_student_data = self.valid_student_data.copy()
        del invalid_student_data['is_council_member']
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)

    def test_missing_is_banned(self):
        invalid_student_data = self.valid_student_data.copy()
        del invalid_student_data['is_banned']
        with self.assertRaises(ValidationError):
            Student(**invalid_student_data)


if __name__ == '__main__':
    unittest.main()
