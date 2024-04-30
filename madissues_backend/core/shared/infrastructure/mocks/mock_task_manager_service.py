from madissues_backend.core.shared.application.task_manager_service import TaskManagerService, TaskManagerServiceFactory
from madissues_backend.core.shared.domain.task_manager import TaskManager


class MockTaskManagerService(TaskManagerService):
    def is_api_key_valid(self, token: str) -> bool:
        if token.startswith("mock-"): return True
        return False


class MockTaskManagerServiceFactory(TaskManagerServiceFactory):
    def get_task_manager_by_name(self, name: str) -> TaskManagerService:
        return MockTaskManagerService()
