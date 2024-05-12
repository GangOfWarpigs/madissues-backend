from sqlalchemy.orm import Session

from madissues_backend.core.students.application.ports.student_query_repository import StudentQueryRepository
from madissues_backend.core.students.domain.read_model.student_read_model import StudentReadModel


# Import the sqlalchemy model


class PostgresStudentQueryRepository(StudentQueryRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_token(self, token: str) -> StudentReadModel | None:
        pass

    def get_by_id(self, token: str) -> StudentReadModel | None:
        pass

