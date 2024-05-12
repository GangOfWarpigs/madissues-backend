from abc import ABC, abstractmethod
from datetime import datetime

from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class IssueCommentRepository(GenericRepository[GenericUUID, IssueComment], ABC):
    @abstractmethod
    def add(self, issue: IssueComment):
        pass

    @abstractmethod
    def remove(self, issue_id: GenericUUID):
        pass

    @abstractmethod
    def get_by_id(self, issue_id: GenericUUID) -> IssueComment | None:
        pass

    @abstractmethod
    def save(self, entity: IssueComment):
        pass
