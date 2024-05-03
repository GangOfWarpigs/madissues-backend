import unittest
from unittest.mock import Mock
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerFactory, TaskManagerService
from madissues_backend.core.task_manager.domain.task_manager import TaskManager
from madissues_backend.core.task_manager.domain.board import Board

class TestTaskManagerValueObjects(unittest.TestCase):
    def setUp(self):
        self.mock_factory = Mock(spec=TaskManagerFactory)
        self.mock_service = Mock(spec=TaskManagerService)
        self.mock_factory.of.return_value = self.mock_service
        self.mock_service.create_empty_board.return_value = "123e4567-e89b-12d3-a456-426614174000"
        self.mock_service.create_empty_list.return_value = "list_id"

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            TaskManager(
                id="invalid_id",
                organization_id=GenericUUID.next_id(),
                config=TaskManagerConfig(service="trello", api_key="test_key")
            )

    def test_invalid_organization_id(self):
        with self.assertRaises(ValueError):
            TaskManager(
                id=GenericUUID.next_id(),
                organization_id="invalid_organization_id",
                config=TaskManagerConfig(service="trello", api_key="test_key")
            )

    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            TaskManager(
                id=GenericUUID.next_id(),
                organization_id=GenericUUID.next_id(),
                config="invalid_config"
            )

    def test_invalid_service_in_config(self):
        with self.assertRaises(ValueError):
            TaskManager(
                id=GenericUUID.next_id(),
                organization_id=GenericUUID.next_id(),
                config=TaskManagerConfig(service="invalid_service", api_key="test_key")
            )

    def test_invalid_api_key_in_config(self):
        with self.assertRaises(ValueError):
            TaskManager(
                id=GenericUUID.next_id(),
                organization_id=GenericUUID.next_id(),
                config=TaskManagerConfig(service="trello", api_key="")
            )

    def test_invalid_board_id(self):
        with self.assertRaises(ValueError):
            Board(
                id="invalid_id",
                queued_list_id="list_id",
                in_progress_list_id="list_id",
                solved_list_id="list_id",
                not_solved_list_id="list_id"
            )

    def test_invalid_queued_list_id(self):
        with self.assertRaises(ValueError):
            Board(
                id=GenericUUID.next_id(),
                queued_list_id="",
                in_progress_list_id="list_id",
                solved_list_id="list_id",
                not_solved_list_id="list_id"
            )

    def test_invalid_in_progress_list_id(self):
        with self.assertRaises(ValueError):
            Board(
                id=GenericUUID.next_id(),
                queued_list_id="list_id",
                in_progress_list_id="",
                solved_list_id="list_id",
                not_solved_list_id="list_id"
            )

    def test_invalid_solved_list_id(self):
        with self.assertRaises(ValueError):
            Board(
                id=GenericUUID.next_id(),
                queued_list_id="list_id",
                in_progress_list_id="list_id",
                solved_list_id="",
                not_solved_list_id="list_id"
            )

    def test_invalid_not_solved_list_id(self):
        with self.assertRaises(ValueError):
            Board(
                id=GenericUUID.next_id(),
                queued_list_id="list_id",
                in_progress_list_id="list_id",
                solved_list_id="list_id",
                not_solved_list_id=""
            )

if __name__ == '__main__':
    unittest.main()