import unittest

from madissues_backend.core.students.domain.student import Student
from madissues_backend.core.students.domain.student_mother import StudentMother
from madissues_backend.core.students.domain.student_preferences import StudentPreferences
from madissues_backend.core.students.domain.student_profile import StudentProfile


class MyTestCase(unittest.TestCase):
    def test_create_1000_students(self):
        student_mother = StudentMother()
        students = [student_mother.random_student() for _ in range(1000)]
        self.assertEqual(1000, len(students))
        for student in students:
            self.assertIsInstance(student, Student)

    def test_create_1000_student_profiles(self):
        student_mother = StudentMother()
        profiles = [student_mother.random_profile() for _ in range(1000)]
        self.assertEqual(1000, len(profiles))
        for profile in profiles:
            self.assertIsInstance(profile, StudentProfile)

    def test_create_1000_student_preferences(self):
        student_mother = StudentMother()
        preferences = [student_mother.random_preferences() for _ in range(1000)]
        self.assertEqual(1000, len(preferences))
        for preference in preferences:
            self.assertIsInstance(preference, StudentPreferences)


if __name__ == '__main__':
    unittest.main()
