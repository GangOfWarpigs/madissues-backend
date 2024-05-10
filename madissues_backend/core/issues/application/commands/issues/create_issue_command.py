from pydantic import BaseModel

from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, owners_only, students_only
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.storage_service import StorageService
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
    assigned_to: str  # GenericUUID


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
    assigned_to: str  # GenericUUID


@students_only
class CreateIssueCommand(Command[CreateIssueRequest, CreateIssueResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: IssueRepository,
                 storage: StorageService):
        self.authentication_service = authentication_service
        self.repository = repository
        self.storage_service = storage

    def execute(self, request: CreateIssueRequest) -> Response[CreateIssueResponse]:
        # Must assign the issue first to a task manager
        # Must create a card in trello
        # Must notify the task manager via email

       issue = Issue(
            id=GenericUUID.next_id(),
            title=request.title,
            description=request.description,
            details=request.details,
            proofs=request.proofs,
            status=request.status,
            date_time=request.date_time,
            course=GenericUUID(request.course),
            teachers=[GenericUUID(teacher) for teacher in request.teachers],
            student=GenericUUID(request.student),
            assigned_to=GenericUUID(request.assigned_to),
        )
        if request.logo:
            issue.upload_logo(request.logo, self.storage_service)

        self.repository.add(issue)
        return Response.ok(CreateIssueResponse(
            **issue.dict(),
        ))
