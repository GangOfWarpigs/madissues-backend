from pydantic import BaseModel

from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.storage_service import StorageService
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class UpdateIssueInformationRequest(BaseModel):
    issue_id: str  # GenericUUID of the issue to update
    title: str
    description: str
    details: str
    proofs: list[str]
    teachers: list[str]


class UpdateIssueInformationResponse(BaseModel):
    id: str  # ID of the updated issue
    title: str
    description: str
    details: str
    proofs: list[str]
    teachers: list[str]


@students_only
class UpdateIssueInformationCommand(Command[UpdateIssueInformationRequest, Response]):
    def __init__(self, authentication_service: AuthenticationService, issue_repository: IssueRepository,
                 storage_service: StorageService, event_bus: EventBus):
        self.authentication_service = authentication_service
        self.issue_repository = issue_repository
        self.storage_service = storage_service
        self.event_bus = event_bus

    def execute(self, request: UpdateIssueInformationRequest) -> Response:
        issue = self.issue_repository.get_by_id(GenericUUID(request.issue_id))
        if not issue:
            return Response.fail(code=404, message="Issue not found")

        # Verify user authorization to update the issue
        if (GenericUUID(self.authentication_service.get_user_id()) != issue.student_id
                and not self.authentication_service.is_site_admin()):
            return Response.fail(code=401, message="Unauthorized to update this issue")

        # First you delete all the old proofs
        for proof in issue.proofs:
            try:
                self.storage_service.delete_image(folder="issues", image_name=proof)
            except (FileNotFoundError, ValueError) as e:
                print(f"Error deleting image {proof} from storage: {e}")

        # Then, you upload the new images to the storage service
        new_proof_filenames = []
        for proof in request.proofs:
            filename = self.storage_service.upload_b64_image(image=proof, folder="issues",
                                                             image_name=str(GenericUUID.next_id()))
            new_proof_filenames.append(filename)

        # Update the issue
        issue.update_information(
            title=request.title,
            description=request.description,
            details=request.details,
            proofs=new_proof_filenames,
            teachers=request.teachers
        )

        self.issue_repository.save(issue)
        self.event_bus.notify_all(issue.collect_events())

        return Response.ok(
            UpdateIssueInformationResponse(
                id=str(issue.id),
                title=issue.title,
                description=issue.description,
                details=issue.details,
                proofs=[str(proof) for proof in issue.proofs],
                teachers=[str(teacher) for teacher in issue.teachers]
            )
        )
