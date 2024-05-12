from datetime import datetime
from typing import Dict, Any
from uuid import UUID

from madissues_backend.core.issues.application.ports.issue_query_repository import IssueQueryRepository
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.domain.read_models.issue_read_model import IssueReadModel, IssueStudentReadModel
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockIssueQueryRepository(IssueQueryRepository):

    def __init__(self, db: EntityTable):
        self.db = db
        self._issues: Dict[UUID, Issue] = self.db.tables["issues"]
        self._organization: Dict[UUID, Any] = self.db.tables["organizations"]
        self._students: Dict[UUID, Any] = self.db.tables["students"]

    def get_all_by_organization(self, organization_id: str) -> list[IssueReadModel]:
        issues = []
        for issue in self._issues.values():
            if issue.organization_id == GenericUUID(organization_id):
                issues.append(issue)

        # find organization from organization_id
        if GenericUUID(organization_id) not in self._organization:
            return []

        organization = self._organization[GenericUUID(organization_id)]
        # find all teacher names
        original_teachers = [teacher for teacher in organization.teachers]
        # get teacher names by issue teacher
        final_issues = []
        for issue in issues:
            teachers = []
            for teacher in original_teachers:
                if teacher.id in issue.teachers:
                    teachers.append(teacher.first_name + " " + teacher.last_name)
            # find student that created issue
            student = None
            if issue.student_id in self._students:
                student = self._students[issue.student_id]
                student = IssueStudentReadModel(name=student.first_name + " " + student.last_name,
                                                year=student.started_studies_date.strftime('%Y'))

            # look for course that issue is related to
            course = None
            for course in organization.courses:
                if course.id == issue.course:
                    course = course.name
                    break

            read_model = IssueReadModel.of(issue)
            read_model.course = course
            read_model.teachers = teachers
            read_model.student = student
            final_issues.append(read_model)

        return final_issues

    def get_by_id(self, issue_id: str) -> IssueReadModel:
        return IssueReadModel.of(self._issues[GenericUUID(issue_id)])

    def get_all_by_title(self, title: str) -> list[IssueReadModel]:
        issues = []
        for issue in self._issues.values():
            if issue.title == title:
                issues.append(issue)
        return list(IssueReadModel.of(x) for x in issues)

    def get_all_by_course(self, course_id: str) -> list[IssueReadModel]:
        issues = []
        for issue in self._issues.values():
            if issue.course == GenericUUID(course_id):
                issues.append(issue)
        return list(IssueReadModel.of(x) for x in issues)

    def get_all_by_student(self, student_id: str) -> list[IssueReadModel]:
        issues = []
        for issue in self._issues.values():
            if issue.student_id == GenericUUID(student_id):
                issues.append(issue)
        return list(IssueReadModel.of(x) for x in issues)

    def get_all_by_teacher(self, teacher_id: str) -> list[IssueReadModel]:
        issues = []
        for issue in self._issues.values():
            if GenericUUID(teacher_id) in issue.teachers:
                issues.append(issue)
        return list(IssueReadModel.of(x) for x in issues)

    def get_all_by_status(self, status: str) -> list[IssueReadModel]:
        issues = []
        for issue in self._issues.values():
            if issue.status == status:
                issues.append(issue)
        return list(IssueReadModel.of(x) for x in issues)

    def get_all(self) -> list[IssueReadModel]:
        return list(IssueReadModel.of(x) for x in self._issues.values())

    def get_all_by_date_greater_than(self, date: str) -> list[IssueReadModel]:
        issues = []
        for issue in self._issues.values():
            if issue.date_time > datetime.strptime(date, '%Y-%m-%d'):
                issues.append(issue)

        return list(IssueReadModel.of(x) for x in issues)

    def get_all_by_date_less_than(self, date: str) -> list[IssueReadModel]:
        issues = []
        for issue in self._issues.values():
            if issue.date_time < datetime.strptime(date, '%Y-%m-%d'):
                issues.append(issue)

        return list(IssueReadModel.of(x) for x in issues)
