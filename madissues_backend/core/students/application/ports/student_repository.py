from abc import ABC, abstractmethod

from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.entity import EntityId
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.domain.student import Student


class StudentRepository(GenericRepository[GenericUUID, Student], ABC):

    @abstractmethod
    def add(self, student: Student):
        pass

    @abstractmethod
    def remove(self, student_id: EntityId):
        pass

    @abstractmethod
    def get_by_id(self, student_id: EntityId) -> Student:
        pass

    @abstractmethod
    def save(self, student: Student):
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Student | None:
        pass

    @abstractmethod
    def get_by_token(self, token: str) -> Student | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Student]:
        pass

    @abstractmethod
    def get_by_organization(self, organization_id: GenericUUID) -> list[Student]:
        pass

    @abstractmethod
    def exists_with_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def can_student_join_organization(self, organization_id: GenericUUID) -> bool:
        pass



