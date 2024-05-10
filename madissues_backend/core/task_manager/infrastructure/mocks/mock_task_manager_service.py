from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerService, TaskManagerFactory
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class InMemoryTaskManagerService(TaskManagerService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.boards: dict = {}
        self.lists: dict = {}
        self.invited_users: list = []

    def is_api_key_valid(self) -> bool:
        return self.api_key == "valid_api_key"

    def get_board_id(self, board_name: str) -> str:
        for board_id, name in self.boards.items():
            if name == board_name:
                return str(board_id)
        return None

    def get_boards_in_organization(self, board_name: str) -> list[str]:
        return [str(board_id) for board_id, name in self.boards.items() if name == board_name]

    def create_organization(self, name: str) -> str:
        organization_id = GenericUUID.next_id()
        self.boards[organization_id] = name
        return str(organization_id)

    def delete_organization(self, organization_id: str):
        del self.boards[organization_id]

    def create_empty_board(self, organization_id: str, name: str) -> str:
        board_id = GenericUUID.next_id()
        self.boards[board_id] = name
        return str(board_id)

    def create_empty_list(self, board_id: str, name: str) -> str:
        list_id = GenericUUID.next_id()
        self.lists[list_id] = {"board_id": board_id, "name": name}
        return str(list_id)

    def invite_user(self, organization_id: str, email: str):
        self.invited_users.append(email)


class MockTaskManagerFactory(TaskManagerFactory):
    def of(self, config: TaskManagerConfig) -> TaskManagerService:
        return InMemoryTaskManagerService(config.api_key)
