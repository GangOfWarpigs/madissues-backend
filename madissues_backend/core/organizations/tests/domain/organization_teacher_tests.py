import unittest
from pydantic import ValidationError
from madissues_backend.core.organizations.domain.organization_teacher import OrganizationTeacher
from madissues_backend.core.shared.domain.value_objects import GenericUUID

class TestOrganizationTeachers(unittest.TestCase):
    def setUp(self):
        self.valid_teacher_data = {
            'id': GenericUUID.next_id(),
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'office_link': 'https://www.dis.ulpgc.es/teacher1',
            'courses': [GenericUUID.next_id(), GenericUUID.next_id()]
        }

    def test_valid_teacher(self):
        teacher = OrganizationTeacher(**self.valid_teacher_data)
        self.assertIsInstance(teacher, OrganizationTeacher)

    def test_invalid_first_name_min_length(self):
        invalid_teacher_data = self.valid_teacher_data.copy()
        invalid_teacher_data['first_name'] = ''
        with self.assertRaises(ValidationError):
            OrganizationTeacher(**invalid_teacher_data)

    def test_invalid_email_format(self):
        invalid_teacher_data = self.valid_teacher_data.copy()
        invalid_teacher_data['email'] = 'invalid_email.com'
        with self.assertRaises(ValidationError):
            OrganizationTeacher(**invalid_teacher_data)

    def test_valid_ulpgc_email_formats(self):
        valid_teacher_data = self.valid_teacher_data.copy()

        valid_teacher_data['email'] = 'profesor@alu.ulpgc.es'
        teacher = OrganizationTeacher(**valid_teacher_data)
        self.assertIsInstance(teacher, OrganizationTeacher)

        valid_teacher_data['email'] = 'profesor.profe@alu.ulpgc.es'
        teacher = OrganizationTeacher(**valid_teacher_data)
        self.assertIsInstance(teacher, OrganizationTeacher)

        valid_teacher_data['email'] = 'profesor103@ulpgc.es'
        teacher = OrganizationTeacher(**valid_teacher_data)
        self.assertIsInstance(teacher, OrganizationTeacher)


    def test_invalid_office_link_format(self):
        invalid_teacher_data = self.valid_teacher_data.copy()
        invalid_teacher_data['office_link'] = 'https://example.com/teacher1'
        with self.assertRaises(ValidationError):
            OrganizationTeacher(**invalid_teacher_data)

    def test_valid_optional_email(self):
        valid_teacher_data_optional_email = self.valid_teacher_data.copy()
        valid_teacher_data_optional_email['email'] = None
        teacher = OrganizationTeacher(**valid_teacher_data_optional_email)
        self.assertIsInstance(teacher, OrganizationTeacher)

    def test_valid_optional_office_link(self):
        valid_teacher_data_optional_link = self.valid_teacher_data.copy()
        valid_teacher_data_optional_link['office_link'] = None
        teacher = OrganizationTeacher(**valid_teacher_data_optional_link)
        self.assertIsInstance(teacher, OrganizationTeacher)

    def test_invalid_courses_type(self):
        invalid_teacher_data = self.valid_teacher_data.copy()
        invalid_teacher_data['courses'] = 'invalid_type'
        with self.assertRaises(ValidationError):
            OrganizationTeacher(**invalid_teacher_data)

    def test_invalid_course(self):
        invalid_teacher_data = self.valid_teacher_data.copy()
        invalid_teacher_data['courses'] = ['a', 'b']
        with self.assertRaises(ValidationError):
            OrganizationTeacher(**invalid_teacher_data)

if __name__ == '__main__':
    unittest.main()
