import unittest
from typing import ClassVar

from pydantic import BaseModel

from madissues_backend.core.issues.application.commands.comments.add_comment_to_issue import AddCommentToIssueCommand
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_comment_repository import MockIssueCommentRepository
from madissues_backend.core.shared.application.event_handler import EventHandler
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_organization_created")
        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        self.issue_comment_repository = MockIssueCommentRepository(self.db)
        self.command = AddCommentToIssueCommand(
            authentication_service=self.authentication_service,
            issue_comment_repository=self.issue_comment_repository
        )
        self.event_bus = MockEventBus()

    def test_subscribed_event_handler_handles_event(self):
        class TestEventPayload(BaseModel):
            payload: str

        class TestEvent(DomainEvent[TestEventPayload]):
            name: ClassVar[str] = "@test/event"
            payload: TestEventPayload

        class MockEventHandler(EventHandler[TestEventPayload]):
            event_name: ClassVar[str] = "@test/event"
            handled: bool = False

            def handle(self, event: TestEventPayload):
                self.handled = True

        mock_event_handler = MockEventHandler()
        self.event_bus.subscribe(
            handler=mock_event_handler,
        )
        self.event_bus.notify(TestEvent(payload=TestEventPayload(payload="test")))

        self.assertTrue(mock_event_handler.handled)


if __name__ == '__main__':
    unittest.main()
