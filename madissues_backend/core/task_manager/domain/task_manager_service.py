from abc import ABC, abstractmethod

from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig


class TaskManagerService(ABC):
    @abstractmethod
    def is_api_key_valid(self) -> bool:
        ...

    @abstractmethod
    def create_empty_board(self, name: str) -> str:
        ...

    @abstractmethod
    def create_empty_list(self, board_id: str, name: str) -> str:
        ...

    @abstractmethod
    def invite_user(self, email: str):
        ...


class TaskManagerFactory(ABC):
    @abstractmethod
    def of(self, config: TaskManagerConfig) -> TaskManagerService:
        ...
