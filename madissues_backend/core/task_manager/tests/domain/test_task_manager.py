import unittest
from unittest.mock import Mock, MagicMock
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerFactory, TaskManagerService
from madissues_backend.core.task_manager.domain.task_manager import TaskManager
from madissues_backend.core.task_manager.domain.board import Board

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.mock_factory = Mock(spec=TaskManagerFactory)
        self.mock_service = Mock(spec=TaskManagerService)
        self.mock_factory.of.return_value = self.mock_service
        self.mock_service.create_empty_board.return_value = "123e4567-e89b-12d3-a456-426614174000"
        self.mock_service.create_empty_list.return_value = "list_id"
        self.task_manager = TaskManager(
            id=GenericUUID.next_id(),
            organization_id=GenericUUID.next_id(),
            config=TaskManagerConfig(service="trello", api_key="test_key")
        )
    def test_generate_infrastructure(self):
        self.task_manager.generate_infrastructure(self.mock_factory)
        self.mock_factory.of.assert_called_once_with(self.task_manager.config)
        self.mock_service.create_empty_board.assert_any_call("faqs")
        self.mock_service.create_empty_board.assert_any_call("issues")
        self.assertEqual(self.mock_service.create_empty_list.call_count, 8)
        self.assertIsNotNone(self.task_manager.faqs_board)
        self.assertIsNotNone(self.task_manager.issue_board)

    def test_generate_idle_board(self):
        board = self.task_manager.generate_idle_board("test", self.mock_service)
        self.mock_service.create_empty_board.assert_called_once_with("test")
        self.assertEqual(self.mock_service.create_empty_list.call_count, 4)
        self.assertIsNotNone(board)

    def test_generate_idle_board_with_different_name(self):
        board = self.task_manager.generate_idle_board("different_test", self.mock_service)
        self.mock_service.create_empty_board.assert_called_once_with("different_test")
        self.assertEqual(self.mock_service.create_empty_list.call_count, 4)
        self.assertIsNotNone(board)

    def test_generate_infrastructure_with_different_config(self):
        self.task_manager.config = TaskManagerConfig(service="trello", api_key="different_test_key")
        self.task_manager.generate_infrastructure(self.mock_factory)
        self.mock_factory.of.assert_called_once_with(self.task_manager.config)
        self.mock_service.create_empty_board.assert_any_call("faqs")
        self.mock_service.create_empty_board.assert_any_call("issues")
        self.assertEqual(self.mock_service.create_empty_list.call_count, 8)
        self.assertIsNotNone(self.task_manager.faqs_board)
        self.assertIsNotNone(self.task_manager.issue_board)

    def test_generate_idle_board_with_different_service(self):
        self.mock_service2 = Mock(spec=TaskManagerService)
        self.mock_service2.create_empty_board.return_value = "123e4567-e89b-12d3-a456-426614174000"
        self.mock_service2.create_empty_list.return_value = "list_id2"
        board = self.task_manager.generate_idle_board("test", self.mock_service2)
    def test_generate_infrastructure_with_same_config(self):
        self.task_manager.generate_infrastructure(self.mock_factory)
        self.task_manager.generate_infrastructure(self.mock_factory)
        self.mock_factory.of.assert_called_with(self.task_manager.config)
        self.mock_service.create_empty_board.assert_any_call("faqs")
        self.mock_service.create_empty_board.assert_any_call("issues")
        self.assertEqual(self.mock_service.create_empty_list.call_count, 16)
        self.assertIsNotNone(self.task_manager.faqs_board)
        self.assertIsNotNone(self.task_manager.issue_board)

    def test_generate_infrastructure_with_same_service(self):
        self.task_manager.generate_infrastructure(self.mock_factory)
        self.task_manager.generate_infrastructure(self.mock_factory)
        self.mock_factory.of.assert_called_with(self.task_manager.config)
        self.mock_service.create_empty_board.assert_any_call("faqs")
        self.mock_service.create_empty_board.assert_any_call("issues")
        self.assertEqual(self.mock_service.create_empty_list.call_count, 16)
        self.assertIsNotNone(self.task_manager.faqs_board)
        self.assertIsNotNone(self.task_manager.issue_board)

if __name__ == '__main__':
    unittest.main()