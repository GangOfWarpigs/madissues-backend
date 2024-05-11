from abc import ABC, abstractmethod

from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.domain.task_manager import TaskManager


class TaskManagerRepository(GenericRepository[GenericUUID, TaskManager], ABC):
    @abstractmethod
    def check_can_integrate_organization(self, organization_id, user_id) -> bool:
        ...

    @abstractmethod
    def is_there_a_task_manager_for_organization(self, organization_id : str) -> bool:
        ...

    @abstractmethod
    def get_by_organization_id(self, organization_id: str) -> TaskManager | None:
        ...

    @abstractmethod
    def get_organization(self, organization_id: str):
        ...
