from typing import Optional

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository
from madissues_backend.core.students.domain.student import Student
from madissues_backend.core.students.infrastructure.postgres.models.student_model import PostgresStudentModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


# Import the sqlalchemy model


class PostgresStudentRepository(StudentRepository):
    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def map_to_model(entity: Student) -> PostgresStudentModel:
        return PostgresStudentModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            details=entity.details,
            proofs=entity.proofs,
            status=entity.status,
            date_time=entity.date_time,
            course=entity.course,
            teachers=entity.teachers,
            student_id=entity.student_id,
            organization_id=entity.organization_id
        )

    def add(self, student: Student) -> None:
        self._session.add(PostgresStudentRepository.map_to_model(student))
        try:
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            raise e

    def remove(self, id: GenericUUID) -> None:
        student = self.get_by_id(id)
        if student:
            self._session.delete(student)
            self._session.commit()

    def get_by_id(self, id: GenericUUID) -> Optional[Student]:
        return self._session.query(PostgresStudentModel).filter(PostgresStudentModel.id == id).first()

    def save(self, student: Student) -> None:
        try:
            self._session.get(PostgresStudentModel, student.id)
            self._session.merge(PostgresStudentRepository.map_to_model(student))
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            raise e
