from pip._internal.utils import datetime
from pydantic import BaseModel

from madissues_backend.core.issues.domain.issue import Issue


class IssueReadModel(BaseModel):
    title: str
    description: str
    details: str
    proofs: list[str]  # List of image links
    status: str  # Queued, In progress, Solved, Not Solved
    date_time: str
    course: str
    teachers: list[str]
    student_id: str

    @staticmethod
    def of(issue: Issue) -> 'IssueReadModel':
        return IssueReadModel(
            title=issue.title,
            description=issue.description,
            details=issue.details,
            proofs=issue.proofs,
            status=issue.status,
            date_time=issue.date_time.strftime('%Y-%m-%d'),
            course=str(issue.course),
            teachers=[str(teacher) for teacher in issue.teachers],
            student_id=str(issue.student_id)
        )