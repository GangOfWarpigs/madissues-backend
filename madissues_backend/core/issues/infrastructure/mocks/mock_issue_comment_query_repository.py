from datetime import datetime
from typing import Dict
from uuid import UUID

from madissues_backend.core.issues.application.ports.issue_comment_query_repository import IssueCommentQueryRepository
from madissues_backend.core.issues.domain.read_models.issue_comment_read_model import IssueCommentReadModel

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockIssueCommentQueryRepository(IssueCommentQueryRepository):
    def __init__(self, entity_table: EntityTable):
        super().__init__(entity_table)
        self._issue_comments: Dict[UUID, IssueCommentReadModel] = self.entity_table.tables["issue_comments"]

    def get_all(self) -> list[IssueCommentReadModel]:
        return list(self._issue_comments.values())

    def get_all_by_author(self, author_id: GenericUUID) -> list[IssueCommentReadModel]:
        return [issue for issue in self._issue_comments.values() if issue.author == author_id]

    def get_all_by_issue(self, issue_id: GenericUUID) -> list[IssueCommentReadModel]:
        return [issue for issue in self._issue_comments.values() if issue.issue_id == issue_id]

    def get_all_by_response_to(self, response_to_id: GenericUUID) -> list[IssueCommentReadModel]:
        return [issue for issue in self._issue_comments.values() if issue.response_to == response_to_id]

    def get_all_by_date_greater_than(self, date: datetime) -> list[IssueCommentReadModel]:
        return [issue for issue in self._issue_comments.values() if issue.date_time > date]

    def get_all_by_date_less_than(self, date: datetime) -> list[IssueCommentReadModel]:
        return [issue for issue in self._issue_comments.values() if issue.date_time < date]
