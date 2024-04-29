from abc import ABC, abstractmethod

from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class IssueRepository(GenericRepository[GenericUUID, Issue], ABC):
    @abstractmethod
    def exists_with_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Issue | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Issue]:
        pass

    @abstractmethod
    def get_all_by_course(self, course_id: GenericUUID) -> list[Issue]:
        pass

    @abstractmethod
    def get_all_by_student(self, student_id: GenericUUID) -> list[Issue]:
        pass

    @abstractmethod
    def get_all_by_teacher(self, teacher_id: GenericUUID) -> list[Issue]:
        pass

    @abstractmethod
    def get_by_task_manager(self, task_manager_id: GenericUUID) -> list[Issue]:
        pass

    @abstractmethod
    def get_all_by_assigned_to(self, assigned_to_id: GenericUUID) -> list[Issue]:
        pass

    @abstractmethod
    def get_all_by_status(self, status: str) -> list[Issue]:
        pass

    @abstractmethod
    def add(self, organization: Issue):
        pass

    @abstractmethod
    def remove(self, organization_id: GenericUUID):
        pass

    @abstractmethod
    def get_by_id(self, organization_id: GenericUUID) -> Issue:
        pass

    @abstractmethod
    def save(self, entity: Issue):
        pass
