from abc import abstractmethod, ABC

from madissues_backend.core.issues.domain.read_models.issue_read_model import IssueReadModel


class IssueQueryRepository(ABC):
    @abstractmethod
    def get_all_by_organization(self, organization_id: str) -> list[IssueReadModel]:
        ...

    @abstractmethod
    def get_by_id(self, issue_id: str) -> IssueReadModel:
        ...

    @abstractmethod
    def get_all_by_title(self, title: str) -> list[IssueReadModel]:
        ...

    @abstractmethod
    def get_all_by_course(self, course_id: str) -> list[IssueReadModel]:
        ...

    @abstractmethod
    def get_all_by_student(self, student_id: str) -> list[IssueReadModel]:
        ...

    @abstractmethod
    def get_all_by_teacher(self, teacher_id: str) -> list[IssueReadModel]:
        ...

    @abstractmethod
    def get_all_by_status(self, status: str) -> list[IssueReadModel]:
        ...

    @abstractmethod
    def get_all(self) -> list[IssueReadModel]:
        ...

    @abstractmethod
    def get_all_by_date_greater_than(self, date: str) -> list[IssueReadModel]:
        ...

    @abstractmethod
    def get_all_by_date_less_than(self, date: str) -> list[IssueReadModel]:
        ...
