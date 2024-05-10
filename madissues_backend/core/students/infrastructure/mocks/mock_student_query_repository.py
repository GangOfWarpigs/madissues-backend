from typing import Dict

from madissues_backend.core.shared.application.mock_repository import GenericMockRepository, EntityTable
from madissues_backend.core.shared.domain.entity import EntityId
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_query_repository import StudentQueryRepository
from madissues_backend.core.students.application.ports.student_repository import StudentRepository
from madissues_backend.core.students.domain.read_model.student_read_model import StudentReadModel
from madissues_backend.core.students.domain.student import Student


class MockStudentQueryRepository(StudentQueryRepository):
    students: Dict[GenericUUID, Student]

    def __init__(self, entity_table: EntityTable):
        self.entity_table = entity_table
        self.students = self.entity_table.tables["students"]
        self.organizations = self.entity_table.tables["organizations"]

    def get_by_token(self, token: str) -> StudentReadModel | None:
        for student in self.students.values():
            if student.token == token:
                return StudentReadModel.of(student)
        return None
