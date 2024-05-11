import unittest
from datetime import datetime

from madissues_backend.core.issues.application.commands.issues.create_issue_command import \
    CreateIssueCommand, CreateIssueRequest
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService


class TestCreateIssueCommentCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_student_created")
        self.event_bus = MockEventBus()
        self.storage_service = LocalStorageService("../../../../../../media")
        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        self.issue_repository = MockIssueRepository(self.db)

    # TODO: Implement test_create_issue_comment

