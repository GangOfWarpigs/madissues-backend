import unittest

from pydantic import BaseModel

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.domain.task_manager import TaskManager
from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_repository import MockTaskManagerRepository

class TestMockTaskManagerRepository(unittest.TestCase):
    def setUp(self):
        self.entity_table = EntityTable()
        self.repo = MockTaskManagerRepository(self.entity_table)

    def test_add_task_manager(self):
        task_manager_config = TaskManagerConfig(service="trello", api_key="test_key")  # replace with actual values
        task_manager = TaskManager(id=GenericUUID.next_id(), organization_id=GenericUUID.next_id(),
                                   config=task_manager_config)
        self.repo.add(task_manager)
        self.assertEqual(self.repo.task_managers[task_manager.id], task_manager)

    def test_remove_task_manager(self):
        task_manager_config = TaskManagerConfig(service="trello", api_key="test_key")  # replace with actual values
        task_manager = TaskManager(id=GenericUUID.next_id(), organization_id=GenericUUID.next_id(),
                                   config=task_manager_config)
        self.repo.add(task_manager)
        self.repo.remove(task_manager.id)
        self.assertNotIn(task_manager.id, self.repo.task_managers)

    def test_get_by_id(self):
        task_manager_config = TaskManagerConfig(service="trello", api_key="test_key")  # replace with actual values
        task_manager = TaskManager(id=GenericUUID.next_id(), organization_id=GenericUUID.next_id(),
                                   config=task_manager_config)
        self.repo.add(task_manager)
        retrieved_task_manager = self.repo.get_by_id(task_manager.id)
        self.assertEqual(retrieved_task_manager, task_manager)

    def test_save_task_manager(self):
        task_manager_config = TaskManagerConfig(service="trello", api_key="test_key")  # replace with actual values
        task_manager = TaskManager(id=GenericUUID.next_id(), organization_id=GenericUUID.next_id(),
                                   config=task_manager_config)
        self.repo.add(task_manager)
        task_manager.organization_id = GenericUUID.next_id()
        self.repo.save(task_manager)
        self.assertEqual(self.repo.task_managers[task_manager.id].organization_id, task_manager.organization_id)

    def test_check_can_integrate_organization(self):
        organization_id = GenericUUID.next_id()
        owner_id = GenericUUID.next_id()

        # Create a dictionary to represent the organization
        class Organization(Entity[GenericUUID]):
            owner_id: GenericUUID

        self.entity_table.tables["organizations"][organization_id] = Organization(
            id=organization_id,
            owner_id=owner_id
        )
        self.entity_table.tables["owners"][owner_id] = owner_id
        self.assertTrue(self.repo.check_can_integrate_organization(organization_id, owner_id))
    def test_is_there_a_task_manager_for_organization(self):
        task_manager_config = TaskManagerConfig(service="trello", api_key="test_key")  # replace with actual values
        task_manager = TaskManager(id=GenericUUID.next_id(), organization_id=GenericUUID.next_id(),
                                   config=task_manager_config)
        self.repo.add(task_manager)
        self.assertTrue(self.repo.is_there_a_task_manager_for_organization(task_manager.organization_id))

    def test_add_task_manager_already_exists(self):
        task_manager_config = TaskManagerConfig(service="trello", api_key="test_key")  # replace with actual values
        task_manager = TaskManager(id=GenericUUID.next_id(), organization_id=GenericUUID.next_id(),
                                   config=task_manager_config)
        self.repo.add(task_manager)
        with self.assertRaises(ValueError):
            self.repo.add(task_manager)

    def test_remove_task_manager_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.repo.remove(GenericUUID.next_id())

    def test_get_by_id_not_found(self):
        with self.assertRaises(ValueError):
            self.repo.get_by_id(GenericUUID.next_id())

    def test_save_task_manager_not_found(self):
        task_manager_config = TaskManagerConfig(service="trello", api_key="test_key")  # replace with actual values
        task_manager = TaskManager(id=GenericUUID.next_id(), organization_id=GenericUUID.next_id(),
                                   config=task_manager_config)
        with self.assertRaises(ValueError):
            self.repo.save(task_manager)

    def test_check_can_integrate_organization_no_organization(self):
        self.entity_table.tables["students"][GenericUUID.next_id()] = None
        self.assertFalse(self.repo.check_can_integrate_organization(GenericUUID.next_id(), GenericUUID.next_id()))

    def test_check_can_integrate_organization_no_user(self):
        self.entity_table.tables["organizations"][GenericUUID.next_id()] = None
        self.assertFalse(self.repo.check_can_integrate_organization(GenericUUID.next_id(), GenericUUID.next_id()))

    def test_is_there_a_task_manager_for_organization_no_task_manager(self):
        self.assertFalse(self.repo.is_there_a_task_manager_for_organization(GenericUUID.next_id()))

    def test_add_remove_get_by_id_save_sequence(self):
        task_manager_config = TaskManagerConfig(service="trello", api_key="test_key")  # replace with actual values
        task_manager = TaskManager(id=GenericUUID.next_id(), organization_id=GenericUUID.next_id(),
                                   config=task_manager_config)
        self.repo.add(task_manager)
        retrieved_task_manager = self.repo.get_by_id(task_manager.id)
        self.assertEqual(retrieved_task_manager, task_manager)
        task_manager.organization_id = GenericUUID.next_id()
        self.repo.save(task_manager)
        updated_task_manager = self.repo.get_by_id(task_manager.id)
        self.assertEqual(updated_task_manager.organization_id, task_manager.organization_id)
        self.repo.remove(task_manager.id)
        with self.assertRaises(ValueError):
            self.repo.get_by_id(task_manager.id)

    def test_check_can_integrate_organization_no_organization_no_user(self):
        self.assertFalse(self.repo.check_can_integrate_organization(GenericUUID.next_id(), GenericUUID.next_id()))

if __name__ == '__main__':
    unittest.main()