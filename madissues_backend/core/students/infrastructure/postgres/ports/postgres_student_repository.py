from typing import List, Optional, Type

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository
from madissues_backend.core.students.domain.postgres.student_preferences_model import PostgresStudentPreferences
from madissues_backend.core.students.domain.student import Student
from madissues_backend.core.students.domain.student_preferences import StudentPreferences
from madissues_backend.core.students.domain.student_profile import StudentProfile
from madissues_backend.core.students.domain.postgres.student_model import PostgresStudent

from madissues_backend.core.students.domain.postgres.student_profile_model import PostgresStudentProfile


class PostgresStudentRepository(StudentRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, student: Student):
        student_model = self._map_to_model(student)
        self._session.add(student_model)
        self._session.commit()

    def remove(self, student_id: GenericUUID):
        student_model = self._session.query(PostgresStudent).filter_by(id=student_id).one()
        self._session.delete(student_model)
        self._session.commit()

    def get_by_id(self, student_id: GenericUUID) -> Optional[Student]:
        try:
            student_model = self._session.query(PostgresStudent).filter_by(id=student_id).one()
            return self._map_to_entity(student_model)
        except NoResultFound:
            return None

    def save(self, student: Student):
        student_model = self._session.merge(self._map_to_model(student))
        self._session.commit()

    def get_by_email(self, email: str) -> Optional[Student]:
        try:
            student_model = self._session.query(PostgresStudent).filter_by(email=email).one()
            return self._map_to_entity(student_model)
        except NoResultFound:
            return None

    def get_by_token(self, token: str) -> Optional[Student]:
        try:
            student_model = self._session.query(PostgresStudent).filter_by(token=token).one()
            return self._map_to_entity(student_model)
        except NoResultFound:
            return None

    def get_all(self) -> List[Student]:
        student_models = self._session.query(PostgresStudent).all()
        return [self._map_to_entity(model) for model in student_models]

    def get_by_organization(self, organization_id: GenericUUID) -> List[Student]:
        student_models = self._session.query(PostgresStudent).filter_by(organization_id=organization_id).all()
        return [self._map_to_entity(model) for model in student_models]

    def exists_with_email(self, email: str) -> bool:
        return self._session.query(self._session.query(PostgresStudent).filter_by(email=email).exists()).scalar()

    def can_student_join_organization(self, organization_id: GenericUUID) -> bool:
        # Implementar lógica para determinar si un estudiante puede unirse a una organización
        # Esta es solo una función de ejemplo; necesitarás adaptarla a tus reglas de negocio
        return not self._session.query(
            self._session.query(PostgresStudent).filter_by(organization_id=organization_id, is_banned=True).exists()
        ).scalar()

    @staticmethod
    def _map_to_model(student: Student) -> PostgresStudent:
        return PostgresStudent(
            id=student.id,
            organization_id=student.organization_id,
            email=student.email,
            first_name=student.first_name,
            last_name=student.last_name,
            password=student.password,  # Asumimos que la contraseña ya está encriptada si es necesario
            started_studies_date=student.started_studies_date,
            is_site_admin=student.is_site_admin,
            is_council_member=student.is_council_member,
            is_banned=student.is_banned,
            token=student.token,
            profile=PostgresStudentProfile(
                student_id=student.id,
                degree=student.profile.degree,
                joined_courses=student.profile.joined_courses
            ),
            preferences=PostgresStudentPreferences(
                student_id=student.id,
                theme=student.preferences.theme,
                language=student.preferences.language
            )
        )

    @staticmethod
    def _map_to_entity(student_model: Type[PostgresStudent]) -> Student:
        return Student(
            id=student_model.id,
            organization_id=student_model.organization_id,
            email=student_model.email,
            first_name=student_model.first_name,
            last_name=student_model.last_name,
            password="",  # No devolvemos la contraseña
            started_studies_date=student_model.started_studies_date,
            is_site_admin=student_model.is_site_admin,
            is_council_member=student_model.is_council_member,
            is_banned=student_model.is_banned,
            token=student_model.token,
            profile=StudentProfile(
                degree=student_model.profile.degree,
                joined_courses=student_model.profile.joined_courses
            ),
            preferences=StudentPreferences(
                theme=student_model.preferences.theme,
                language=student_model.preferences.language
            )
        )

