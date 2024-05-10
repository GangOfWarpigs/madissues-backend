from datetime import datetime

from pydantic import BaseModel

from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.issues.domain.events.issue_created import IssueCreated, IssueCreatedPayload
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class CreateIssueRequest(BaseModel):
    title: str
    description: str
    details: str
    proofs: list[str]  # List of image links
    status: str  # Queued, In progress, Solved, Not Solved
    date_time: str
    course: str  # GenericUUID
    teachers: list[str]  # list[GenericUUID]
    student: str  # GenericUUID


class CreateIssueResponse(BaseModel):
    title: str
    description: str
    details: str
    proofs: list[str]  # List of image links
    status: str  # Queued, In progress, Solved, Not Solved
    date_time: str
    course: str  # GenericUUID
    teachers: list[str]  # list[GenericUUID]
    student: str  # GenericUUID


@students_only
class CreateIssueCommand(Command[CreateIssueRequest, CreateIssueResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: IssueRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.repository = repository
        self.event_bus = event_bus

    def execute(self, request: CreateIssueRequest) -> Response[CreateIssueResponse]:
        """
            - Must assign the issue first to a task manager
            - Must create a card in trello
            - Must notify the task manager via email
        """
        issue = Issue(
            id=GenericUUID.next_id(),
            title=request.title,
            description=request.description,
            details=request.details,
            proofs=request.proofs,
            status=request.status,
            date_time=datetime.strptime(request.date_time, '%Y-%m-%d'),
            course=GenericUUID(request.course),
            teachers=[GenericUUID(teacher) for teacher in request.teachers],
            student_id=GenericUUID(request.student),
        )

        issue.register_event(IssueCreated(
            payload=IssueCreatedPayload(
                title=issue.title,
                description=issue.description,
                details=issue.details,
                proofs=issue.proofs,
                status=issue.status,
                date_time=issue.date_time.strftime('%Y-%m-%d'),
                course=str(issue.course),
                teachers=[str(teacher) for teacher in issue.teachers],
                student=str(issue.student_id),
            )
        ))
        self.event_bus.notify_all(issue.collect_events())

        self.repository.add(issue)

        return Response.ok(CreateIssueResponse(
            **issue.dict(),
        ))
