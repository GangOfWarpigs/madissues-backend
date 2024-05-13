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

    def add(self, student: Student):
        # Mapeamos y añadimos las entidades relacionadas primero
        student_profile = self._map_profile_to_model(student.profile, student.id)
        student_preferences = self._map_preferences_to_model(student.preferences, student.id)

        student_model = self._map_to_model(student)
        self._session.add(student_model)
        self._session.flush()  # Esto asegura que las entidades se guarden en la base de datos y se asignen los IDs

        # Añadimos y guardamos las dependencias
        self._session.add(student_profile)
        self._session.add(student_preferences)

        # Ahora mapeamos y añadimos el estudiante principal

        self._session.commit()

    @staticmethod
    def _map_to_model(student: Student) -> PostgresStudent:
        print("MAPPING TO MODEL ------------------------->")
        print(student)
        return PostgresStudent(
            id=str(student.id),
            organization_id=str(student.organization_id),
            email=student.email,
            first_name=student.first_name,
            last_name=student.last_name,
            password=student.password,
            started_studies_date=student.started_studies_date,
            is_site_admin=student.is_site_admin,
            is_council_member=student.is_council_member,
            is_banned=student.is_banned,
            token=student.token
            # Nota: Las relaciones de `profile` y `preferences` son manejadas por SQLAlchemy
        )

    @staticmethod
    def _map_profile_to_model(profile: StudentProfile, student_id: GenericUUID) -> PostgresStudentProfile:
        return PostgresStudentProfile(
            student_id=student_id,
            degree_id=profile.degree,
        )

    @staticmethod
    def _map_preferences_to_model(preferences: StudentPreferences,
                                  student_id: GenericUUID) -> PostgresStudentPreferences:
        return PostgresStudentPreferences(
            student_id=str(student_id),
            theme=preferences.theme,
            language=preferences.language
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
