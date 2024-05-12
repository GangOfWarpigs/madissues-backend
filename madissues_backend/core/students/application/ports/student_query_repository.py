from abc import ABC, abstractmethod

from madissues_backend.core.students.domain.read_model.student_read_model import StudentReadModel
from madissues_backend.core.students.domain.student import Student


class StudentQueryRepository(ABC):
    @abstractmethod
    def get_by_token(self, token: str) -> StudentReadModel | None:
        ...

    @abstractmethod
    def get_by_id(self, token: str) -> StudentReadModel | None:
        ...
