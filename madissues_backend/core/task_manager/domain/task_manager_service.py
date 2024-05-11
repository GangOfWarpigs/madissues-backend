from abc import ABC, abstractmethod
from typing import Any

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
    def get_board_lists(self, board_id: str) -> list[str]:
        ...

    @abstractmethod
    def get_board_list_by_name(self, board_id: str, list_name: str) -> str | None:
        ...

    @abstractmethod
    def get_list_cards(self, list_id: str) -> list[str]:
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
    def get_board_by_name_in_organization(self, organization_id_or_name: str, board_name: str) -> str | None:
        ...

    @abstractmethod
    def create_organization(self, name: str) -> str:
        ...

    @abstractmethod
    def get_organization(self, organization_id_or_name: str) -> Any:
        ...

    @abstractmethod
    def delete_organization(self, organization_id: str):
        ...

    @abstractmethod
    def create_card(self, list_id: str, name: str, description: str) -> str:
        ...

    @abstractmethod
    def get_card(self, card_id: str) -> str:
        ...

    @abstractmethod
    def update_card(self, card_id: str, name: str, description: str) -> str:
        ...


class TaskManagerFactory(ABC):
    @abstractmethod
    def of(self, config: TaskManagerConfig) -> TaskManagerService:
        ...
