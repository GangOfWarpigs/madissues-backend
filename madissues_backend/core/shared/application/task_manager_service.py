from abc import abstractmethod, ABC

from madissues_backend.core.shared.domain.task_manager import TaskManager


class TaskManagerService(ABC):
    @abstractmethod
    def is_api_key_valid(self, token: str) -> bool:
        ...

    @abstractmethod
    def create_basic_board(self, name: str) -> str:
        ...

    @abstractmethod
    def create_basic_list(self, name: str) -> str:
        ...


class TaskManagerServiceFactory(ABC):
    @abstractmethod
    def get_task_manager_by_name(self, name: TaskManager) -> TaskManagerService:
        ...
