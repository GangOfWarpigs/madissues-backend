from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerService, TaskManagerFactory


class InMemoryTaskManagerService(TaskManagerService):
    def __init__(self):
        self.api_key = "valid_api_key"
        self.boards = {}
        self.lists = {}
        self.invited_users = []

    def is_api_key_valid(self) -> bool:
        return self.api_key == "valid_api_key"

    def create_empty_board(self, name: str) -> str:
        board_id = str(len(self.boards) + 1)
        self.boards[board_id] = name
        return board_id

    def create_empty_list(self, board_id: str, name: str) -> str:
        list_id = str(len(self.lists) + 1)
        self.lists[list_id] = {"board_id": board_id, "name": name}
        return list_id

    def invite_user(self, email: str):
        self.invited_users.append(email)


class InMemoryTaskManagerFactory(TaskManagerFactory):
    def of(self, config: TaskManagerConfig) -> TaskManagerService:
        return InMemoryTaskManagerService()