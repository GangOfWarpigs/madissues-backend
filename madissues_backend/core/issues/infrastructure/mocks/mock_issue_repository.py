from abc import ABC
from typing import Optional, Dict
from uuid import UUID

from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.shared.application.mock_repository import GenericMockRepository, EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockIssueRepository(IssueRepository, GenericMockRepository[UUID, Issue]):
    def __init__(self, entity_table: EntityTable):
        super().__init__(entity_table)
        self._issues: Dict[UUID, Issue] = self.entity_table.tables["issues"]

    def add(self, issue: Issue) -> Issue:
        self._issues[issue.id] = issue
        return issue

    def save(self, issue: Issue) -> Issue:
        if issue.id not in self._issues:
            raise ValueError(f"Issue with id {issue.id} does not exist")
        self._issues[issue.id] = issue
        return issue

    def remove(self, issue_id: GenericUUID):
        if issue_id not in self._issues:
            raise ValueError(f"Issue with id {issue_id} does not exist")
        del self._issues[issue_id]

    def get_by_id(self, issue_id: GenericUUID) -> Optional[Issue]:
        return self._issues.get(issue_id)
 