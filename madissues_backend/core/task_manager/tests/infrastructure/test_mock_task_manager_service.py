import unittest

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.infrastructure.mocks.mock_task_manager_service import \
    InMemoryTaskManagerService, MockTaskManagerFactory


class TestInMemoryTaskManagerService(unittest.TestCase):
    def setUp(self):
        self.service = InMemoryTaskManagerService("valid_api_key")

    def test_is_api_key_valid(self):
        self.assertTrue(self.service.is_api_key_valid())

    def test_create_empty_list(self):
        list_id = self.service.create_empty_list("1", "test_list")
        self.assertEqual(len(self.service.lists), 1)

    def test_invite_user(self):
        self.service.invite_user(str(GenericUUID.next_id()), "test@example.com")
        self.assertIn("test@example.com", self.service.invited_users)

    def test_create_multiple_boards(self):
        for i in range(5):
            board_id = self.service.create_empty_board(str(GenericUUID.next_id()), f"test_board_{i}")

        assert len(self.service.boards) == 5

    def test_create_multiple_lists(self):
        for i in range(5):
            list_id = self.service.create_empty_list("1", f"test_list_{i}")

        assert len(self.service.lists) == 5

    def test_invite_multiple_users(self):
        emails = [f"test{i}@example.com" for i in range(5)]
        for email in emails:
            self.service.invite_user(GenericUUID.next_id(), email)
        for email in emails:
            self.assertIn(email, self.service.invited_users)


class TestInMemoryTaskManagerFactory(unittest.TestCase):
    def setUp(self):
        self.factory = MockTaskManagerFactory()

    def test_of(self):
        service = self.factory.of(TaskManagerConfig(service="trello", api_key="test_key", token="test_token"))
        self.assertIsInstance(service, InMemoryTaskManagerService)

    def test_of_with_different_configs(self):
        services = [self.factory.of(
            TaskManagerConfig(
                service=f"trello",
                api_key=f"key{i}",
                token=f"token{i}"
            )) for i in range(5)]
        for service in services:
            self.assertIsInstance(service, InMemoryTaskManagerService)


if __name__ == '__main__':
    unittest.main()
