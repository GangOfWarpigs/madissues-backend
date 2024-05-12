from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from madissues_backend.core.students.domain.postgres.student_model import PostgresStudent
from madissues_backend.core.students.domain.read_model.student_read_model import StudentReadModel


class PostgresStudentQueryRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_token(self, token: str) -> Optional[StudentReadModel]:
        try:
            student_model = self._session.query(PostgresStudent)\
                .filter(PostgresStudent.token == token).one()
            return self._map_to_read_model(student_model)
        except NoResultFound:
            return None

    def get_by_id(self, student_id: str) -> Optional[StudentReadModel]:
        try:
            student_model = self._session.query(PostgresStudent)\
                .filter(PostgresStudent.id == student_id).one()
            return self._map_to_read_model(student_model)
        except NoResultFound:
            return None

    @staticmethod
    def _map_to_read_model(student_model: PostgresStudent) -> StudentReadModel:
        # Assuming the existence of PostgresStudentProfile and PostgresStudentPreferences are handled here:
        profile = student_model.profile if hasattr(student_model, 'profile') else None
        preferences = student_model.preferences if hasattr(student_model, 'preferences') else None

        return StudentReadModel(
            id=str(student_model.id),
            organization_id=str(student_model.organization_id),
            email=str(student_model.email),
            first_name=str(student_model.first_name),
            last_name=str(student_model.last_name),
            password=str(student_model.password),  # Consider omitting or securely handling the password
            started_studies_date=student_model.started_studies_date.isoformat(),
            is_site_admin=bool(student_model.is_site_admin),
            is_council_member=bool(student_model.is_council_member),
            is_banned=bool(student_model.is_banned),
            degree=str(profile.degree) if profile else None,
            joined_courses=[str(course) for course in profile.joined_courses] if profile and profile.joined_courses else [],
            theme=preferences.theme if preferences else None,
            language=preferences.language if preferences else None
        )

