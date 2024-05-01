from typing import Dict

from madissues_backend.core.shared.application.mock_repository import GenericMockRepository, EntityTable
from madissues_backend.core.shared.domain.entity import EntityId
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository
from madissues_backend.core.students.domain.student import Student


class MockStudentRepository(StudentRepository, GenericMockRepository[GenericUUID, Student]):
    students: Dict[GenericUUID, Student]

    def __init__(self, entity_table: EntityTable):
        super().__init__(entity_table)
        self.students = self.entity_table.tables["students"]
        self.organizations = self.entity_table.tables["organizations"]

    def add(self, student: Student):
        if self.students.get(student.id):
            raise ValueError("Student already exists")
        self.students[student.id] = student

    def remove(self, student_id: EntityId):
        if not self.students.get(student_id):
            raise ValueError("Student does not exists")
        del self.students[student_id]

    def get_by_id(self, student_id: EntityId) -> Student:
        student = self.students.get(student_id)
        if not student:
            raise ValueError("Student not found")
        return student

    def save(self, student: Student):
        index = self.students.get(student.id)
        if index is None:
            raise ValueError("Student not found")
        self.students[student.id] = student

    def get_by_email(self, email: str) -> Student | None:
        for student in self.students.values():
            if student.email == email:
                return student
        return None

    def get_by_token(self, token: str) -> Student | None:
        for student in self.students.values():
            if student.token == token:
                return student
        return None

    def get_all(self) -> list[Student]:
        return list(self.students.values())

    def get_by_organization(self, organization_id: GenericUUID) -> list[Student]:
        return [student for student in self.students.values() if student.organization_id == organization_id]

    def exists_with_email(self, email: str) -> bool:
        for student in self.students.values():
            if student.email == email:
                return True
        return False

    def can_student_join_organization(self, organization_id: GenericUUID) -> bool:
        organization = self.organizations.get(organization_id)
        if not organization:
            return False
        return True
