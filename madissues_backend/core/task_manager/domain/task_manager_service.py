from abc import ABC, abstractmethod

from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig


class TaskManagerService(ABC):
    @abstractmethod
    def is_api_key_valid(self) -> bool:
        ...

    @abstractmethod
    def create_empty_board(self, organization_id: str, name: str) -> str:
        ...

    @abstractmethod
    def create_empty_list(self, board_id: str, name: str) -> str:
        ...

    @abstractmethod
    def invite_user(self, organization_id: str, email: str):
        ...

    @abstractmethod
    def get_board_id(self, board_name: str) -> str:
        ...

    @abstractmethod
    def get_boards_in_organization(self, board_name: str) -> list[str]:
        ...

    @abstractmethod
    def create_organization(self, name: str) -> str:
        ...

    @abstractmethod
    def delete_organization(self, organization_id: str):
        ...


class TaskManagerFactory(ABC):
    @abstractmethod
    def of(self, config: TaskManagerConfig) -> TaskManagerService:
        ...
