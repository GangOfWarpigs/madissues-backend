from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerService, TaskManagerFactory
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class InMemoryTaskManagerService(TaskManagerService):
    def __init__(self, api_key):
        self.api_key = api_key
        self.boards = {}
        self.lists = {}
        self.invited_users = []

    def is_api_key_valid(self) -> bool:
        return self.api_key == "valid_api_key"

    def create_empty_board(self, name: str) -> str:
        board_id = GenericUUID.next_id()
        self.boards[board_id] = name
        return str(board_id)

    def create_empty_list(self, board_id: str, name: str) -> str:
        list_id = GenericUUID.next_id()
        self.lists[list_id] = {"board_id": board_id, "name": name}
        return str(list_id)

    def invite_user(self, email: str):
        self.invited_users.append(email)


class InMemoryTaskManagerFactory(TaskManagerFactory):
    def of(self, config: TaskManagerConfig) -> TaskManagerService:
        return InMemoryTaskManagerService(config.api_key)
