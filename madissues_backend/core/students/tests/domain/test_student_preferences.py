import unittest
from pydantic import ValidationError

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.domain.student_preferences import StudentPreferences


class TestStudentPreferences(unittest.TestCase):
    def test_valid_preferences(self):
        valid_preferences_data = {
            'id': GenericUUID.next_id(),
            'theme': 'Dark',
            'language': 'en'
        }
        preferences = StudentPreferences(**valid_preferences_data)
        self.assertIsInstance(preferences, StudentPreferences)

    def test_invalid_theme(self):
        invalid_preferences_data = {
            'id': GenericUUID.next_id(),
            'theme': 'InvalidTheme',
            'language': 'en'
        }
        with self.assertRaises(ValidationError):
            StudentPreferences(**invalid_preferences_data)

    def test_valid_language(self):
        valid_preferences_data = {
            'id': GenericUUID.next_id(),
            'theme': 'Dark',
            'language': 'ES'
        }
        preferences = StudentPreferences(**valid_preferences_data)
        self.assertIsInstance(preferences, StudentPreferences)

        valid_preferences_data['language'] = 'ESP'
        preferences = StudentPreferences(**valid_preferences_data)
        self.assertIsInstance(preferences, StudentPreferences)

    def test_invalid_language(self):
        invalid_preferences_data = {
            'id': GenericUUID.next_id(),
            'theme': 'Dark',
            'language': 'invalid'
        }
        with self.assertRaises(ValidationError):
            StudentPreferences(**invalid_preferences_data)


if __name__ == '__main__':
    unittest.main()
