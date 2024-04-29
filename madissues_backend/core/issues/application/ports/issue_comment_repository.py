from abc import ABC, abstractmethod
from datetime import datetime

from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class IssueCommentRepository(GenericRepository[GenericUUID, IssueComment], ABC):

    @abstractmethod
    def get_all(self) -> list[IssueComment]:
        pass

    @abstractmethod
    def get_all_by_author(self, author_id: GenericUUID) -> list[IssueComment]:
        pass

    @abstractmethod
    def get_all_by_issue(self, issue_id: GenericUUID) -> list[IssueComment]:
        pass

    @abstractmethod
    def get_all_by_response_to(self, response_to_id: GenericUUID) -> list[IssueComment]:
        pass

    @abstractmethod
    def get_all_by_date_greater_than(self, date: datetime) -> list[IssueComment]:
        pass

    @abstractmethod
    def get_all_by_date_less_than(self, date: datetime) -> list[IssueComment]:
        pass

    @abstractmethod
    def add(self, issue: IssueComment):
        pass

    @abstractmethod
    def remove(self, issue_id: GenericUUID):
        pass

    @abstractmethod
    def get_by_id(self, issue_id: GenericUUID) -> IssueComment:
        pass

    @abstractmethod
    def save(self, entity: IssueComment):
        pass
