from abc import ABC
from typing import Optional, Dict
from uuid import UUID

from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.shared.application.mock_repository import GenericMockRepository, EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockIssueRepository(IssueRepository, GenericMockRepository[UUID, Issue], ABC):
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

    def get_by_name(self, name: str) -> Optional[Issue]:
        for issue in self._issues.values():
            if issue.name == name:
                return issue
        return None

    def exists_with_name(self, name: str) -> bool:
        for issue in self._issues.values():
            if issue.name == name:
                return True
        return False

    def get_all(self) -> list[Issue]:
        return list(self._issues.values())

    def get_all_by_course(self, course_id: GenericUUID) -> list[Issue]:
        return [issue for issue in self._issues.values() if issue.course == course_id]

    def get_all_by_student(self, student_id: GenericUUID) -> list[Issue]:
        return [issue for issue in self._issues.values() if issue.student == student_id]

    def get_all_by_teacher(self, teacher_id: GenericUUID) -> list[Issue]:
        return [issue for issue in self._issues.values() if teacher_id in issue.teachers]

    def get_by_task_manager(self, task_manager_id: GenericUUID) -> list[Issue]:
        return [issue for issue in self._issues.values() if issue.task_manager_id == task_manager_id]

    def get_all_by_assigned_to(self, assigned_to_id: GenericUUID) -> list[Issue]:
        return [issue for issue in self._issues.values() if issue.assigned_to == assigned_to_id]

    def get_all_by_status(self, status: str) -> list[Issue]:
        return [issue for issue in self._issues.values() if issue.status == status]





