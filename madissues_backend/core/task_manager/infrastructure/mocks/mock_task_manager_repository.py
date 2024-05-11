from typing import Dict

from madissues_backend.core.shared.application.mock_repository import GenericMockRepository, EntityTable
from madissues_backend.core.shared.domain.entity import EntityId
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.domain.task_manager import TaskManager
from madissues_backend.core.task_manager.application.ports.task_manager_repository import TaskManagerRepository

class MockTaskManagerRepository(TaskManagerRepository, GenericMockRepository[GenericUUID, TaskManager]):
    task_managers: Dict[GenericUUID, TaskManager]

    def __init__(self, entity_table: EntityTable):
        super().__init__(entity_table)
        self.task_managers = self.entity_table.tables["task_managers"]
        self.organizations = self.entity_table.tables["organizations"]
        self.owners = self.entity_table.tables["owners"]

    def add(self, task_manager: TaskManager):
        if self.task_managers.get(task_manager.id):
            raise ValueError("TaskManager already exists")
        self.task_managers[task_manager.id] = task_manager

    def remove(self, task_manager_id: EntityId):
        if not self.task_managers.get(task_manager_id):
            raise ValueError("TaskManager does not exist")
        del self.task_managers[task_manager_id]

    def get_by_id(self, task_manager_id: EntityId) -> TaskManager:
        task_manager = self.task_managers.get(task_manager_id)
        if not task_manager:
            raise ValueError("TaskManager not found")
        return task_manager

    def save(self, task_manager: TaskManager):
        index = self.task_managers.get(task_manager.id)
        if index is None:
            raise ValueError("TaskManager not found")
        self.task_managers[task_manager.id] = task_manager

    def check_can_integrate_organization(self, organization_id: str, owner_id: str) -> bool:
        organization = self.organizations.get(GenericUUID(organization_id))
        if not organization or str(organization.owner_id) != str(owner_id):
            return False
        return True

    def is_there_a_task_manager_for_organization(self, organization_id : str) -> bool:
        for task_manager in self.task_managers.values():
            if str(task_manager.organization_id) == organization_id:
                return True
        return False

    def get_by_organization_id(self, organization_id: str) -> TaskManager | None:
        for task_manager in self.task_managers.values():
            if str(task_manager.organization_id) == organization_id:
                return task_manager
        return None

    def get_organization(self, organization_id: str):
        return self.organizations.get(GenericUUID(organization_id))


