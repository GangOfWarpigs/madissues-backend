import unittest
from pydantic import ValidationError
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse
from madissues_backend.core.shared.domain.value_objects import GenericUUID

class TestOrganizationCourse(unittest.TestCase):
    def setUp(self):
        self.valid_course_data = {
            'id': GenericUUID.next_id(),
            'name': 'Test Course',
            'code': 'TEST1234',
            'icon': 'ion-home',
            'primary_color': '#e400ff',
            'secondary_color': '#0049ff',
        }

    def test_valid_course(self):
        course = OrganizationCourse(**self.valid_course_data)
        print("Course: ", course)
        self.assertIsInstance(course, OrganizationCourse)

    def test_invalid_name_min_length(self):
        invalid_course_data = self.valid_course_data.copy()
        invalid_course_data['name'] = 'A'
        with self.assertRaises(ValidationError):
            OrganizationCourse(**invalid_course_data)

    def test_invalid_code_max_length(self):
        invalid_course_data = self.valid_course_data.copy()
        invalid_course_data['code'] = '123456789'
        with self.assertRaises(ValidationError):
            OrganizationCourse(**invalid_course_data)

    def test_no_icon(self):
        invalid_course_data = self.valid_course_data.copy()
        invalid_course_data['icon'] = ''
        with self.assertRaises(ValidationError):
            OrganizationCourse(**invalid_course_data)

    def test_invalid_primary_color_format(self):
        invalid_course_data = self.valid_course_data.copy()
        invalid_course_data['primary_color'] = '#invalid'
        with self.assertRaises(ValidationError):
            OrganizationCourse(**invalid_course_data)

    def test_invalid_secondary_color_format(self):
        invalid_course_data = self.valid_course_data.copy()
        invalid_course_data['secondary_color'] = '#invalid'
        with self.assertRaises(ValidationError):
            OrganizationCourse(**invalid_course_data)

    # Agrega más pruebas para otros casos de validez o invalidez según sea necesario

if __name__ == '__main__':
    unittest.main()
