from abc import ABC, abstractmethod

from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class IssueRepository(GenericRepository[GenericUUID, Issue], ABC):
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
