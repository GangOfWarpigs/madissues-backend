import unittest
from uuid import uuid4

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.domain.student_mother import StudentMother
from madissues_backend.core.students.infrastructure.mocks.mock_student_repository import MockStudentRepository


class TestMockStudentRepository(unittest.TestCase):
    def setUp(self):
        self.entity_table = EntityTable()
        self.entity_table.tables["students"] = {}
        self.repo = MockStudentRepository(self.entity_table)
        # Añadir algunos estudiantes de prueba
        self.student1 = StudentMother.random_student()
        self.student2 = StudentMother.random_student()
        self.repo.add(self.student1)
        self.repo.add(self.student2)

    def test_add_student_success(self):
        new_student = StudentMother.random_student()
        self.repo.add(new_student)
        self.assertIn(new_student.id, self.repo.students)

    def test_add_student_failure(self):
        with self.assertRaises(ValueError):
            self.repo.add(self.student1)  # Intentar añadir el mismo estudiante nuevamente

    def test_remove_student_success(self):
        self.repo.remove(self.student1.id)
        self.assertNotIn(self.student1.id, self.repo.students)

    def test_remove_student_failure(self):
        with self.assertRaises(ValueError):
            self.repo.remove(GenericUUID(str(uuid4())))  # ID no existente

    def test_get_by_id_success(self):
        student = self.repo.get_by_id(self.student1.id)
        self.assertEqual(student, self.student1)

    def test_get_by_id_failure(self):
        with self.assertRaises(ValueError):
            self.repo.get_by_id(GenericUUID(str(uuid4())))  # ID no existente

    def test_save_student_success(self):
        self.student1.email = "updated@example.com"
        self.repo.save(self.student1)
        updated_student = self.repo.get_by_id(self.student1.id)
        self.assertEqual(updated_student.email, "updated@example.com")

    def test_save_student_failure(self):
        new_student = StudentMother.random_student()
        with self.assertRaises(ValueError):
            self.repo.save(new_student)  # Intentar guardar un estudiante no existente

    def test_get_by_email_success(self):
        student = self.repo.get_by_email(self.student1.email)
        self.assertEqual(student, self.student1)

    def test_get_by_email_failure(self):
        self.assertIsNone(self.repo.get_by_email("nonexistent@example.com"))

    def test_get_by_token_success(self):
        student = self.repo.get_by_token(self.student1.token)
        self.assertEqual(student, self.student1)

    def test_get_by_token_failure(self):
        self.assertIsNone(self.repo.get_by_token("invalid_token"))

    def test_get_all(self):
        students = self.repo.get_all()
        self.assertEqual(len(students), 2)  # Debe haber dos estudiantes

    def test_get_by_organization_success(self):
        organization_id = self.student1.organization_id
        students = self.repo.get_by_organization(organization_id)
        self.assertTrue(any(s for s in students if s.organization_id == organization_id))

    def test_exists_with_email(self):
        self.assertTrue(self.repo.exists_with_email(self.student1.email))
        self.assertFalse(self.repo.exists_with_email("nonexistent@example.com"))

    def test_change_student_preferences(self):
        student = self.repo.get_by_id(self.student1.id)
        new_preferences = StudentMother.random_preferences()
        student.preferences = new_preferences
        self.repo.save(student)
        updated_student = self.repo.get_by_id(self.student1.id)
        self.assertEqual(updated_student.preferences, new_preferences)

    def test_change_student_profile(self):
        student = self.repo.get_by_id(self.student1.id)
        new_profile = StudentMother.random_profile()
        student.profile = new_profile
        self.repo.save(student)
        updated_student = self.repo.get_by_id(self.student1.id)
        self.assertEqual(updated_student.profile, new_profile)


if __name__ == '__main__':
    unittest.main()
