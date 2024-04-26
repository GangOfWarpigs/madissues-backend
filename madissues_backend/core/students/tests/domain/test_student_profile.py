import unittest

from pydantic import ValidationError

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.domain.student_profile import StudentProfile


class TestStudentProfile(unittest.TestCase):
    def test_valid_student_profile(self):
        valid_profile_data = {
            'id': GenericUUID.next_id(),
            'degree': GenericUUID.next_id(),
            'joined_courses': [GenericUUID.next_id(), GenericUUID.next_id()]
        }
        profile = StudentProfile(**valid_profile_data)
        self.assertIsInstance(profile, StudentProfile)

    def test_missing_degree(self):
        invalid_profile_data = {
            'id': GenericUUID.next_id(),
            'joined_courses': [GenericUUID.next_id(), GenericUUID.next_id()]
        }
        with self.assertRaises(ValidationError):
            StudentProfile(**invalid_profile_data)

    def test_missing_joined_courses(self):
        invalid_profile_data = {
            'id': GenericUUID.next_id(),
            'degree': GenericUUID.next_id()
        }
        with self.assertRaises(ValidationError):
            StudentProfile(**invalid_profile_data)

    def test_invalid_joined_courses(self):
        invalid_profile_data = {
            'id': GenericUUID.next_id(),
            'degree': GenericUUID.next_id(),
            'joined_courses': ['a', 'b', 'c']
        }
        with self.assertRaises(ValidationError):
            StudentProfile(**invalid_profile_data)

    def test_empty_joined_courses(self):
        invalid_profile_data = {
            'id': GenericUUID.next_id(),
            'degree': GenericUUID.next_id(),
            'joined_courses': []
        }
        student_profile = StudentProfile(**invalid_profile_data)
        self.assertIsInstance(student_profile, StudentProfile)

    def test_invalid_joined_courses_type(self):
        invalid_profile_data = {
            'id': GenericUUID.next_id(),
            'degree': GenericUUID.next_id(),
            'joined_courses': 'invalid_type'
        }
        with self.assertRaises(ValidationError):
            StudentProfile(**invalid_profile_data)


if __name__ == '__main__':
    unittest.main()
