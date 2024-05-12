from abc import ABC, abstractmethod
from datetime import datetime

from madissues_backend.core.issues.domain.read_models.issue_comment_read_model import IssueCommentReadModel
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class IssueCommentQueryRepository(ABC):

    def __init__(self, entity_table: EntityTable):
        self.entity_table = entity_table

    @abstractmethod
    def get_all(self) -> list[IssueCommentReadModel]:
        pass

    @abstractmethod
    def get_all_by_author(self, author_id: GenericUUID) -> list[IssueCommentReadModel]:
        pass

    @abstractmethod
    def get_all_by_issue(self, issue_id: GenericUUID) -> list[IssueCommentReadModel]:
        pass

    @abstractmethod
    def get_all_by_response_to(self, response_to_id: GenericUUID) -> list[IssueCommentReadModel]:
        pass

    @abstractmethod
    def get_all_by_date_greater_than(self, date: datetime) -> list[IssueCommentReadModel]:
        pass

    @abstractmethod
    def get_all_by_date_less_than(self, date: datetime) -> list[IssueCommentReadModel]:
        pass
