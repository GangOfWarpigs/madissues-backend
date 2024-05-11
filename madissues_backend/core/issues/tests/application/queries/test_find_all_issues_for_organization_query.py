import unittest
from datetime import datetime

from madissues_backend.core.issues.application.commands.issues.create_issue_command import \
    CreateIssueCommand, CreateIssueRequest
from madissues_backend.core.issues.application.queries.find_all_issues_for_organization_query import FindAllIssuesQuery, \
    FindAllIssuesQueryParams
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_query_repository import MockIssueQueryRepository
from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService


class TestFindAllIssuesQuery(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.db.load_snapshot("with_student_created")
        self.event_bus = MockEventBus()
        self.storage_service = LocalStorageService("../../../../../../media")
        self.student = self.db.tables['students'][GenericUUID("fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")]
        self.authentication_service = create_mock_authentication_service(self.db)(self.student.token)
        self.issue_repository = MockIssueRepository(self.db)
        self.issue_query_repository = MockIssueQueryRepository(self.db)

    def tearDown(self):
        self.event_bus.events = []

    def test_find_all_issues_by_organization(self):
        # Create some issues
        create_command = CreateIssueCommand(self.authentication_service,
                                            self.issue_repository,
                                            self.storage_service,
                                            self.event_bus)

        create_response_1 = create_command.run(CreateIssueRequest(
            title="Test Issue 1",
            description="Description of the test issue 1",
            details="Additional details",
            proofs=[],
            status="Queued",
            date_time=datetime.now().strftime('%Y-%m-%d'),
            course="c0517ecb-24e5-4d5e-841c-48b7001e5f94",
            teachers=["d93ab3a5-7cb0-4a23-9327-ae15c2481675"],
            student="1d372590-a034-4e05-b1e8-02a9e91068f3",
            organization_id="fa68b53a-8db6-4f5b-9d15-e93cbc163bfa"
        ))

        create_response_2 = create_command.run(CreateIssueRequest(
            title="Test Issue 2",
            description="Description of the test issue 2",
            details="Additional details",
            proofs=[],
            status="Queued",
            date_time=datetime.now().strftime('%Y-%m-%d'),
            course="c0517ecb-24e5-4d5e-841c-48b7001e5f94",
            teachers=["d93ab3a5-7cb0-4a23-9327-ae15c2481675"],
            student="1d372590-a034-4e05-b1e8-02a9e91068f3",
            organization_id="fa68b53a-8db6-4f5b-9d15-e93cbc163bfa"
        ))

        # Find issues by organization
        query = FindAllIssuesQuery(self.authentication_service, self.issue_query_repository)
        params = FindAllIssuesQueryParams(organization_id="fa68b53a-8db6-4f5b-9d15-e93cbc163bfa")
        query_response = query.execute(params)

        assert query_response.is_success() is True, "Query must be successful"
        assert len(query_response.success) == 2, "Two issues must be found"

    def test_find_all_issues_by_organization_unauthorized_user(self):
        unauthorized_token = "fa68b53a-8db6-4f5b-9d15-e93cbc163bf0"
        self.authentication_service = create_mock_authentication_service(self.db)(unauthorized_token)
        query = FindAllIssuesQuery(self.authentication_service, self.issue_query_repository)
        params = FindAllIssuesQueryParams(organization_id="c0517ecb-24e5-4d5e-841c-48b7001e5f94")
        query_response = query.run(params)

        assert query_response.is_error() is True, "Query must fail"
        assert query_response.error.error_code == 403, "Error code must indicate 'forbidden'"
        assert query_response.error.error_message == "User must be authenticated", "Error message must indicate 'forbidden'"
