from abc import ABC, abstractmethod

from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class IssueRepository(GenericRepository[GenericUUID, Issue], ABC):
    pass
