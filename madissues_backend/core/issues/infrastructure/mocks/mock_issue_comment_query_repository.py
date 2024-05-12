from datetime import datetime
from typing import Dict
from uuid import UUID

from madissues_backend.core.issues.application.ports.issue_comment_query_repository import IssueCommentQueryRepository
from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.issues.domain.read_models.issue_comment_read_model import IssueCommentReadModel
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockIssueCommentQueryRepository(IssueCommentQueryRepository):
    def __init__(self, entity_table: EntityTable):
        super().__init__(entity_table)
        self._issue_comments: Dict[UUID, IssueComment] = self.entity_table.tables["issue_comments"]

    def get_by_id(self, issue_id: GenericUUID) -> IssueCommentReadModel | None:
        issue = self._issue_comments.get(issue_id)
        if issue:
            return IssueCommentReadModel.of(issue)
        return None

    def get_all(self) -> list[IssueCommentReadModel]:
        return list(IssueCommentReadModel.of(issue_comment) for issue_comment in self._issue_comments.values())

    def get_all_by_author(self, author_id: GenericUUID) -> list[IssueCommentReadModel]:
        return [IssueCommentReadModel.of(issue_comment) for issue_comment in self._issue_comments.values() if
                issue_comment.author == author_id]

    def get_all_by_issue(self, issue_id: GenericUUID) -> list[IssueCommentReadModel]:
        return [IssueCommentReadModel.of(issue_comment) for issue_comment in self._issue_comments.values() if
                issue_comment.issue_id == issue_id]

    def get_all_by_response_to(self, response_to_id: GenericUUID) -> list[IssueCommentReadModel]:
        return [IssueCommentReadModel.of(issue_comment) for issue_comment in self._issue_comments.values() if
                issue_comment.response_to == response_to_id]

    def get_all_by_date_greater_than(self, date: datetime) -> list[IssueCommentReadModel]:
        return [IssueCommentReadModel.of(issue_comment) for issue_comment in self._issue_comments.values() if
                issue_comment.date_time > date]

    def get_all_by_date_less_than(self, date: datetime) -> list[IssueCommentReadModel]:
        return [IssueCommentReadModel.of(issue_comment) for issue_comment in self._issue_comments.values() if
                issue_comment.date_time < date]
